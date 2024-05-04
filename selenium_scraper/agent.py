"""A wrapper class for the selenium webdriver, allows creating and managing a driver with the desired parameters"""
import json
import time

import seleniumbase
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_scraper.driver_utils import check, find, parse, scroll, utils, wait

save_url = """old_wop = window.open; function new_wop(url) { document.g_url = url }; window.open = new_wop"""


class Agent:
    """Agent managing a Selenium WebDriver, provides utility methods for locating elements. Uses a seleniumbase
    driver internally.
    """
    def __init__(
            self,
            proxy: str | None,  # USER:PASS@SERVER:PORT
            headless: bool,
            undetected: bool,
            user_data_dir: str,
            browser: str = "chrome",
            scroll_timeout: float = 30.0,
            wait_timeout: float = 60.0,
            redirect_timeout: float = 3.0,
            check_timeout: float = 1.0,
    ) -> None:
        """
        Create a new Agent

        :param str proxy: Set a proxy in the following format, 'USER:PASS@SERVER:PORT' or set to None to disable
        NOTE: some proxies might not work in https mode and only work with http instead
        :param bool headless: Activate headless mode
        :param bool undetected: Enable the undected version of the seleniumbase driver
        :param str user_data_dir: Path to the user data directory, set to None to not use one
        :param str browser: Which browser to use ("chrome", "safari", etc.), must be installed on your device.
        :param float scroll_timeout: The timeout used to wait in scroll-utility methods
        :param float wait_timeout: Timeout used to wait utility methods (e.g. wait_until_exists(), ... )
        :param float redirect_timeout: Timeout used to wait for a redirect link to load
        :param check_timeout: Timeout used in check-related utiliy methods (e.g. check_if_exists(), ... )
        """
        self.proxy = proxy
        self.undetected = undetected
        self.headless = headless
        self.user_data_dir = user_data_dir

        self.scroll_timeout = scroll_timeout
        self.wait_timeout = wait_timeout
        self.check_timeout = check_timeout
        self.redirect_timeout = redirect_timeout
        self.driver: WebDriver | None = None
        self.browser = browser

    # start the driver
    def start(self, **kwargs):
        """start a selenium webdriver using seleniumbase, if you want more control, override this method and call the
        seleniumbase.Driver() method yourself, or pass in additonal keyword args."""
        self.driver = seleniumbase.Driver(
            browser=self.browser,
            proxy=self.proxy,
            headless=self.headless,
            undetected=self.undetected,
            undetectable=self.undetected,
            user_data_dir=self.user_data_dir,
            **kwargs
        )
        self.driver.start_client()

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
        return scroll.into_view(driver=self.driver, body=body, element=element,
                                window_height=self.driver.get_window_size()["height"])

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
