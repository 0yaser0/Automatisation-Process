from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

class TikTokLoginAutomation:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = None

    def login(self):
        print("Initializing Chrome WebDriver...")
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

        print("Opening TikTok login page...")
        self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
        time.sleep(5)

        print("Entering email...")
        email_input = self.driver.find_element(By.NAME, 'username')
        email_input.send_keys(self.email)

        print("Entering password...")
        password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password_input.send_keys(self.password)

        print("Submitting login form...")
        password_input.send_keys(Keys.ENTER)

        print("Waiting for login to process...")
        time.sleep(10)

        print("Closing the browser...")
        self.driver.quit()
        print("Login process completed.")