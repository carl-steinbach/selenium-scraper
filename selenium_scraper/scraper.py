"""A specialized agent used to structure web scraping"""
import time

import selenium_scraper.user_agent
from selenium_scraper.agent import Agent
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
            headless: bool,
            verbose: bool,
            dry_run: bool,
            enable_stealth: bool,
            window: Window | None,
            user_data_dir: str | None,
            low_data: bool,
    ) -> None:
        super().__init__(
            user_agent=user_agent,
            proxy_country=proxy_country,
            proxy_config=proxy_config,
            headless=headless,
            window=window,
            enable_stealth=enable_stealth,
            user_data_dir=user_data_dir,
            low_data=low_data
        )
        self.dry_run = dry_run
        self.name = name
        self.verbose = verbose

    def log(self, msg):
        print(f"[{self.name}] {msg}")

    def info(self, msg):
        if self.verbose:
            self.log(msg)
