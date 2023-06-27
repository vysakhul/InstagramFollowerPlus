import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import random


SIMILAR_ACCOUNT = "Account id similar to yours goes here"
USERNAME = "username"
PASSWORD = "password"

# Avoid very high numbers to prevent flagging by Instagram
FOLLOWERS_TO_SCAN = 60


class InstaFollower:
    def __init__(self):
        self.opt = Options()
        self.opt.add_experimental_option("detach", True)
        self.serv = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.serv, options=self.opt)
        self.driver.maximize_window()

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(10)
        self.driver.find_element(By.NAME, "username").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(10)
        try:
            if self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Turn on Notifications')]").is_displayed():
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
        except NoSuchElementException:
            pass

    def find_followers(self):
        self.driver.get("https://www.instagram.com/" + SIMILAR_ACCOUNT + "/")
        time.sleep(10)
        self.driver.find_element(By.XPATH, "//div[contains(text(), 'followers')]").click()
        time.sleep(10)
        # Follower list only load more names after we scroll to the end of each scroll bar
        # So first we need to make a few scrolls to preload a huge list of elements and then grab the list
        self.follow_btns = self.driver.find_elements(By.XPATH, "//div[@class='_aano']//button")
        while len(self.follow_btns) < FOLLOWERS_TO_SCAN:
            webdriver.ActionChains(self.driver).move_to_element(self.follow_btns[-1]).perform()
            time.sleep(2)
            self.follow_btns = self.driver.find_elements(By.XPATH, "//div[@class='_aano']//button")
            time.sleep(2)
        print(f"Number of Follower accounts captured: {len(self.follow_btns)}")

    def follow(self):
        count = 0
        for btn in self.follow_btns:
            self.driver.execute_script("arguments[0].focus();", btn)
            if btn.text == "Follow" and btn.is_enabled():
                btn.click()
                count += 1
            time.sleep(random.randint(2, 4))
        print(f"{count} followers added")


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()

# CODE UPGRADE POSSIBILITY: The follower list scan module can be updated to find just follow buttons and ignore
# accounts that were already added/following/requested. So we can ask the program to add n number of followers
# as of now, when we scan n number of users there is no guarantee about how many are new on the list