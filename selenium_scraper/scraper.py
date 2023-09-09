"""A specialized agent used to structure web scraping"""
import traceback

from selenium_scraper.agent import Agent
from selenium_scraper.credentials import Credentials
from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.user_agent import UserAgent


class Scraper(Agent):
    def __init__(
            self, name: str,
            user_agent: UserAgent,
            proxy_country: str,
            proxy_config: ProxyConfig,
            credentials: Credentials,
            headless: bool,
            max_retries: int,
            window_size: tuple[int, int],
            window_position: tuple[int, int]
    ) -> None:
        super().__init__(
            user_agent=user_agent,
            proxy_country=proxy_country,
            proxy_config=proxy_config,
            headless=headless,
            window_position=window_position,
            window_size=window_size
        )
        self.name = name
        self.credentials = credentials
        self.max_retries = max_retries
        self.retries = 0
        self.iterations = 100

    # requires an active driver
    def setup(self):
        # navigate to the desired location, log in etc.
        pass

    # requires setup to be complete
    def scrape(self):
        # collect the actual data
        pass

    def run(self):
        while True:
            try:
                self.start()
                self.setup()
                for iteration in range(self.iterations):
                    self.scrape()
                    print(f"----------------- {iteration} \\ {self.iterations} ------------------")
            except KeyboardInterrupt:
                self.quit()
                exit(1)
            except Exception:
                print(traceback.format_exc())
                self.quit()

    def run_once(self):
        try:
            self.start()
            self.setup()
            for iteration in range(self.iterations):
                self.scrape()
                print(f"----------------- {iteration} \\ {self.iterations} ------------------")
        except KeyboardInterrupt:
            self.quit()
            exit(1)
        except Exception:
            print(traceback.format_exc())

        try:
            self.quit()
        except:
            return

    def log(self, msg):
        print(f"[{self.name}] {msg}")
