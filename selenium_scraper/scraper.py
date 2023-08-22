from selenium_scraper.user_agent import UserAgent
from selenium_scraper.credentials import Credentials
from selenium_scraper.driver import chrome
from selenium_scraper.agent import Agent
from selenium_scraper.proxy.config import ProxyConfig


# manages a web scraper interface that allows setup and execution of data mining
class Scraper(Agent):
    def __init__(
            self, name: str, user_agent: UserAgent, 
            proxy_name: str, proxy_config: ProxyConfig, 
            credentials: Credentials, headless: bool, 
            window_size: tuple[int], 
            window_position: tuple[int]
        ) -> None:

        self.name = name
        self.credentials = credentials
        
        super().__init__(
            user_agent=user_agent, 
            proxy_name=proxy_name, 
            proxy_config=proxy_config,
            headless=headless, 
            window_position=window_position, 
            window_size=window_size
        )

    # requires an active driver
    def setup(self):
        # navigate to the desired location, log in etc.
        pass

    # requires setup to be complete
    def scrape(self):
        # collect the actual data
        pass

    def log(self, msg):
        print(f"[{self.name}] {msg}")
