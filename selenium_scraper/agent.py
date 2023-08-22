from selenium_scraper.user_agent import UserAgent
from selenium_scraper.credentials import Credentials
from selenium_scraper.driver import chrome
from selenium.webdriver import Chrome

# manages a webdriver and utility methods
class Agent():
    def __init__(self, user_agent: UserAgent, proxy_name: str=None, headless: bool=False) -> None:
        self.user_agent = user_agent
        self.proxy_name = proxy_name
        self.headless = headless
        self.driver: Chrome = None

    def start(self):
        # start the driver
        self.driver = chrome.create_driver(user_agent=self.user_agent, proxy_name=self.proxy_name, headless=self.headless)

    def quit(self):
        # cleanup resources and stop the driver
        self.driver.quit()