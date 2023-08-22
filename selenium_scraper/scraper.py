from selenium_scraper.user_agent import UserAgent
from selenium_scraper.credentials import Credentials
from selenium_scraper.driver import chrome
from selenium_scraper.agent import Agent


# manages a web scraper interface that allows setup and execution of data mining
class Scraper(Agent):
    def __init__(self, name: str, user_agent: UserAgent, proxy_name: str, credentials: Credentials, headless: bool) -> None:
        self.name = name
        self.credentials = credentials
        # set parameters
        super().__init__(user_agent=user_agent, proxy_name=proxy_name, headless=headless)

    def start(self):
        # start the driver
        self.driver = chrome.create_driver(user_agent=self.user_agent, proxy_name=self.proxy_name, headless=self.headless)

    # requires an active driver
    def setup(self):
        # navigate to the desired location, log in etc.
        pass

    # requires setup to be complete
    def scrape(self):
        # collect the actual data
        pass

    def quit(self):
        # cleanup resources and stop the driver
        self.driver.quit()

    def log(self, msg):
        print(f"[{self.name}] {msg}")