from selenium_scraper.user_agent import UserAgent
from selenium_scraper.credentials import Credentials
from selenium_scraper.driver import chrome


class Scraper():
    def __init__(self, name: str, user_agent: UserAgent, credentials: Credentials=None, proxy_name: str=None, headless: bool=False) -> None:
        self.name = name
        self.user_agent = user_agent
        self.credentials = credentials
        self.proxy_name = proxy_name
        self.headless = headless
        self.driver = None
        # set parameters
        pass

    def start(self):
        # start the driver
        self.driver = chrome.create_driver(user_agent=self.user_agent, proxy_name=self.proxy_name, headless=self.headless)

    def setup(self):
        # navigate to the desired location, log in etc.
        pass

    def scrape(self):
        # collect the actual data
        pass

    def quit(self):
        # cleanup resources and stop the driver
        self.driver.quit()

    def log(self, msg):
        print(f"[{self.name}] {msg}")