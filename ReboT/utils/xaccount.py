from ReboT.constants import *
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class XAccount:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password
        self.cookies = False

    def login(self):
        self.driver.get(XLOGIN)
        sleep(2)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        except TimeoutException:
            print('[!] An error occurred while login in. Refreshing...')
            self.driver.execute_script("window.open('', '_blank');")
            self.driver.close()
            self.driver.switch_to.window(driver.window_handles[1])
            self.driver.get(XLOGIN)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@name='text']")))
        elem = self.driver.find_element(By.XPATH, "//input[@name='text']")
        elem.click()
        elem.send_keys(self.username)
        elem.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        sleep(0.5)
        elem = self.driver.find_element(By.XPATH, "//input[@name='password']")
        elem.send_keys(self.password)
        elem.send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@data-testid='AppTabBar_Profile_Link']")))
        print('[i] Logged in successfully.')

    def view_tweet(self, url):
        self.driver.get(url)
        if self.cookies == False:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Accept all cookies']")))
            self.driver.find_element(By.XPATH, "//*[text()='Accept all cookies']").click()
            self.cookies = True
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, ".//article[@data-testid='tweet' and @tabindex='-1']")))
        tweet = self.driver.find_element(By.XPATH, ".//article[@data-testid='tweet' and @tabindex='-1']")
        return tweet

    def rt(self, tweet):
        if type(tweet) == str:
            tweet = self.view_tweet(tweet)
        try:
            WebDriverWait(tweet, 5).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='retweet']")))
        except TimeoutException:
            print('[!] Unable to repost tweet. Already reposted?')
            return 1
        tweet.find_element(By.XPATH, ".//div[@data-testid='retweet']").click()
        WebDriverWait(tweet, 5).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='retweet']")))
        tweet.find_element(By.XPATH, ".//div[@data-testid='retweetConfirm']").click()
        print('[+] Post Retweeted.')

    def like(self, tweet):
        if type(tweet) == str:
            tweet = self.view_tweet(tweet)
        try:
            WebDriverWait(tweet, 10).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='like']")))
        except TimeoutException:
            print('[!] Unable to like tweet. Already liked?')
            return 1
        WebDriverWait(tweet, 5).until(EC.presence_of_element_located((By.XPATH, ".//div[@data-testid='like']")))
        tweet.find_element(By.XPATH, ".//div[@data-testid='like']").click()
        print('[+] Post liked.')

    def rt_like(self, tweet):
        if type(tweet) == str:
            tweet = self.view_tweet(tweet)
        self.rt(tweet)
        self.like(tweet)
        return tweet