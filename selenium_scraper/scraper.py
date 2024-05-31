"""A specialized agent used to structure web scraping"""
from selenium_scraper.agent import Agent
import sbvirtualdisplay


class Scraper(Agent):
    def __init__(
            self,
            name: str,
            proxy: str | None,
            user_data_dir: str | None,
            undetected: bool,
            headless: bool,
            browser: str = "chrome",
            virtual_display: sbvirtualdisplay.Display | None = None,
            scroll_timeout: int = 30.0,
            wait_timeout: int = 60.0,
            redirect_timeout: int = 3.0,
            check_timeout: int = 1.0,
    ) -> None:
        super().__init__(
            headless=headless,
            user_data_dir=user_data_dir,
            proxy=proxy,
            undetected=undetected,
            scroll_timeout=scroll_timeout,
            wait_timeout=wait_timeout,
            redirect_timeout=redirect_timeout,
            check_timeout=check_timeout,
            browser=browser,
            virtual_display=virtual_display
        )
        self.name = name
