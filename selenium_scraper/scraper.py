"""A specialized agent used to structure web scraping"""
import time
import traceback

import selenium_scraper.user_agent
from selenium_scraper.agent import Agent
from selenium_scraper.credentials import Credentials
from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.user_agent import UserAgent
from selenium_scraper.window import Window


class Scraper(Agent):
    def __init__(
            self,
            name: str,
            user_agent: UserAgent,
            proxy_country: str | None,
            proxy_config: ProxyConfig | None,
            credentials: Credentials | None,
            headless: bool,
            max_retries: int,
            window: Window | None,
            verbose: bool,
            iterations: int,
            enable_stealth: bool,
            user_data_dir: str | None
    ) -> None:
        super().__init__(
            user_agent=user_agent,
            proxy_country=proxy_country,
            proxy_config=proxy_config,
            headless=headless,
            window=window,
            enable_stealth=enable_stealth,
            user_data_dir=user_data_dir
        )
        self.name = name
        self.credentials = credentials
        self.max_retries = max_retries
        self.retries = 0
        self.iterations = iterations
        self.verbose = verbose

    # requires an active driver
    def setup(self):
        """Prepare the scraping session."""
        pass

    # requires setup to be complete
    def scrape(self):
        """Collect and parse data."""
        pass

    def run(self):
        """Let the scraper setup and scrape continuosly until the maximum retries are reached."""
        while True:
            try:
                self.start()
                self.setup()
                for iteration in range(self.iterations):
                    self.scrape()
                    print(
                        f"----------------- "
                        f"[iterations: {iteration}\\{self.iterations}, retries: {self.retries}\\{self.max_retries}]"
                        f"------------------ "
                    )
            except KeyboardInterrupt:
                self.quit()
                exit(1)
            except Exception:
                print(traceback.format_exc())
                self.quit()
                self.retries += 1

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
        except Exception:
            return

    def log(self, msg):
        print(f"[{self.name}] {msg}")

    def info(self, msg):
        if self.verbose:
            self.log(msg)


if __name__ == "__main__":
    scraper = Scraper(
        name="test",
        user_agent=selenium_scraper.user_agent.UserAgent.DESKTOP,
        proxy_config=None,
        proxy_country=None,
        credentials=None,
        headless=False,
        max_retries=3,
        window=Window(height=1800, width=1000, x=50, y=50),
        verbose=True,
        iterations=1,
        enable_stealth=False,
        user_data_dir=None
    )

    scraper.start()
    scraper.driver.get("https://dollah.co")
    time.sleep(60000)
