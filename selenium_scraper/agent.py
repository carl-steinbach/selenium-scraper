"""A wrapper class for the selenium webdriver, allows creating and managing a driver with the desired parameters"""
import json
import time

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement

from selenium_scraper.driver import chrome
from selenium_scraper.driver_utils import wait, find, check, parse, scroll, utils
from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.user_agent import UserAgent
from selenium_scraper.window import Window

save_url = """old_wop = window.open; function new_wop(url) { document.g_url = url }; window.open = new_wop"""


class Agent:
    def __init__(
            self,
            user_agent: UserAgent,
            proxy_country: str | None,
            proxy_config: ProxyConfig | None,
            headless: bool,
            window: Window | None,
            enable_stealth: bool,
            user_data_dir: str | None,
            low_data: bool
    ) -> None:
        self.user_agent = user_agent
        self.proxy_country = proxy_country
        self.proxy_config = proxy_config
        self.headless = headless
        self.window = window
        self.enable_stealth = enable_stealth
        self.user_data_dir = user_data_dir

        self.scroll_timeout = 30.0
        self.wait_timeout = 60.0
        self.check_timeout = 1.0
        self.redirect_timeout = 3.0
        self.driver: Chrome | None = None
        self.low_data: bool = low_data

    # start the driver
    def start(self):
        self.driver = chrome.create_driver(
            user_agent=self.user_agent,
            proxy_country=self.proxy_country,
            proxy_config=self.proxy_config,
            headless=self.headless,
            window=self.window,
            enable_stealth=self.enable_stealth,
            user_data_dir=self.user_data_dir,
            low_data=self.low_data,
            use_undetected_chromedriver=False
        )

    # cleanup resources and stop the driver
    def quit(self):
        self.driver.quit()

    # wait until a condition is fulfilled
    def wait_until_exists(self, locator: tuple, parent: WebElement = None, msg: str = "",
                          number_of_elements: int = None):
        if parent is None and number_of_elements is None:
            return wait.until_exists(driver=self.driver, locator=locator, timeout=self.wait_timeout, msg=msg)
        if parent is not None and number_of_elements is None:
            return wait.until_exists_parent(parent=parent, locator=locator, timeout=self.wait_timeout, msg=msg)
        if parent is None and number_of_elements is not None:
            return wait.until_exists_list(self.driver, locator=locator, timeout=self.wait_timeout, msg=msg,
                                          number_of_elements=number_of_elements)
        if parent is not None and number_of_elements is not None:
            return wait.until_exists_list_parent(parent, locator=locator, timeout=self.wait_timeout, msg=msg,
                                                 number_of_elements=number_of_elements)

    def wait_until_stale(self, element: WebElement, msg: str = ""):
        return wait.until_stale(self.driver, element, self.wait_timeout, msg=msg)

    def wait_until_not_exists(self, locator: tuple, parent: WebElement = None, msg: str = ""):
        root = self.driver
        if parent is not None:
            root = parent

        return wait.until_not_exists(root, locator=locator, timeout=self.wait_timeout, msg=msg)

    def wait_until_clickable(self, element: WebElement, msg: str = ""):
        return wait.until_clickable(self.driver, element=element, timeout=self.wait_timeout, msg=msg)

    def wait_until_invisible(self, element: WebElement, msg: str = ""):
        return wait.until_invisible(driver=self.driver, element=element, timeout=self.wait_timeout, msg=msg)

    def scroll_into_view(self, body: WebElement, element: WebElement):
        return scroll.into_view(driver=self.driver, body=body, element=element, window_height=self.window.height)

    def scroll_until_loaded(self, body: WebElement, locator: tuple, msg: str = ""):
        return scroll.until_loaded(driver=self.driver, body=body, locator=locator, timeout=self.scroll_timeout, msg=msg)

    def scroll_until_timeout(self, body: WebElement):
        return scroll.until_timeout(driver=self.driver, body=body, timeout=self.scroll_timeout)

    # check if an element fulfills a condition
    def check_if_exists(self, locator: tuple, parent: WebElement = None) -> WebElement:
        if parent is not None:
            return check.if_exists_parent(parent=parent, locator=locator, timeout=self.check_timeout)
        else:
            return check.if_exists(driver=self.driver, locator=locator, timeout=self.check_timeout)

    @staticmethod
    def check_if_attribute_exists(element: WebElement, attribute: str) -> str:
        return check.if_attribute_exists(element=element, attribute=attribute)

    def check_if_alert_exists(self, msg: str = ""):
        return check.if_alert_exists(driver=self.driver, timeout=self.check_timeout, msg=msg)

    def check_if_stale(self, element: WebElement, msg: str = "") -> bool:
        return check.if_stale(driver=self.driver, element=element, msg=msg)

    # find elements in different ways
    def find_by_xpath(self, xpath_list: list[str], verbose: bool = False):
        return find.by_xpath(driver=self.driver, xpath_list=xpath_list, verbose=verbose)

    def try_click(self, element: WebElement, msg: str = "") -> bool:
        return utils.try_click(element=element, timeout=self.wait_timeout, msg=msg)

    def get_text(self, element: WebElement, msg: str = "") -> str:
        return parse.get_text(element=element, timeout=self.wait_timeout, msg=msg)

    def get_button_link(self, button: WebElement):
        self.driver.execute_script(save_url)
        button.click()
        url = self.driver.execute_script("return document.g_url")
        return url

    def get_redirects(self, url):
        self.driver.get_log("performance")
        self.driver.get(url)
        requests = []

        while True:
            time.sleep(self.redirect_timeout)
            new_requests = list(filter(self._valid_redirect, self.driver.get_log("performance")))
            if len(new_requests) == 0:
                alert = self.check_if_alert_exists()
                if alert:
                    alert.accept()
                else:
                    break
            else:
                requests += new_requests

        redirect_urls = [r["params"]["url"] for r in requests]
        return redirect_urls

    @staticmethod
    def _valid_redirect(log):
        msg = json.loads(log["message"])["message"]
        if msg["method"] != "Network.responseReceived":
            return False

        if msg["params"]["type"] != "Document":
            return False

        return True
