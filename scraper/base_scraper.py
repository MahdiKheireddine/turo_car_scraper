from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time

class BaseScraper:
    def __init__(self):
        self.driver = None

    def init_driver(self, headless=False):
        options = uc.ChromeOptions()
        options.headless = headless
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=options)

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
