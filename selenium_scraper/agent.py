from selenium_scraper.user_agent import UserAgent
from selenium_scraper.credentials import Credentials
from selenium_scraper.driver import chrome
from selenium.webdriver import Chrome
from selenium_scraper.driver_utils import wait, find, check, parse, scroll, utils
from selenium.webdriver.remote.webelement import WebElement

# manages a webdriver and utility methods
class Agent():
    def __init__(self, user_agent: UserAgent, proxy_name: str=None, headless: bool=False) -> None:
        self.user_agent = user_agent
        self.proxy_name = proxy_name
        self.headless = headless
        self.scroll_timeout = 30.0
        self.wait_timeout = 60.0
        self.check_timeout = 0.1
        self.driver: Chrome = None

    def start(self):
        # start the driver
        self.driver = chrome.create_driver(user_agent=self.user_agent, proxy_name=self.proxy_name, headless=self.headless)

    def quit(self):
        # cleanup resources and stop the driver
        self.driver.quit()

    # wait until a condition is fulfilled
    def wait_until_exists(self, locator: tuple, parent: WebElement=None, msg: str="", number_of_elements: int=None):
        if parent is None and number_of_elements is None:
            return wait.until_exists(self.driver, locator=locator, timeout=self.wait_timeout, msg=msg)
        if parent is not None and number_of_elements is None:
            return wait.until_exists(parent, locator=locator, timeout=self.wait_timeout, msg=msg)
        if parent is None and number_of_elements is not None:
            return wait.until_exists(self.driver, locator=locator, timeout=self.wait_timeout, msg=msg, number_of_elements=number_of_elements)
        if parent is not None and number_of_elements is not None:
            return wait.until_exists(parent, locator=locator, timeout=self.wait_timeout, msg=msg, number_of_elements=number_of_elements)
        
    def wait_until_stale(self, element: WebElement, msg: str=""):
        return wait.until_stale(self.driver, element, self.wait_timeout, msg=msg)

    def wait_until_not_exists(self, locator: tuple, parent: WebElement=None, msg: str=""):
        root = self.driver
        if parent is not None:
            root = parent

        return wait.until_not_exists(root, locator=locator, timeout=self.wait_timeout, msg=msg)
    
    def wait_until_clickable(self, element: WebElement, msg: str=""):
        return wait.until_clickable(self.driver, element=element, timeout=self.wait_timeout, msg=msg)
    
    def wait_until_invisible(self, element: WebElement, msg: str=""):
        return wait.until_invisible(driver=self.driver, element=element, timeout=self.wait_timeout, msg=msg)
    
    def scroll_into_view(self, body: WebElement, element: WebElement, window_height: int):
        return scroll.into_view(driver=self.driver, body=body, element=element, window_height=window_height)
    
    def scroll_until_loaded(self, body: WebElement, locator: tuple, msg: str=""):
        return scroll.until_loaded(driver=self.driver, body=body, locator=locator, timeout=self.scroll_timeout, msg=msg)
    
    def scroll_until_timeout(self, body: WebElement):
        return scroll.until_timeout(driver=self.driver, body=body, timeout=self.scroll_timeout)
    
    # check if an element fulfills a condition
    def check_if_exists(self, locator: tuple, parent: WebElement=None) -> bool:
        if parent is not None:
            return check.if_exists(parent=parent, locator=locator, timeout=self.check_timeout)
        else:
            return check.if_exists(driver=self.driver, locator=locator, timeout=self.check_timeout)
        
    def check_if_attribute_exists(self, element: WebElement, attribute: str) -> bool:
        return check.if_attribute_exists(element=element, attribute=attribute)
    
    def check_if_alert_exists(self, msg: str="") -> bool:
        return check.if_alert_exists(driver=self.driver, timeout=self.check_timeout, msg=msg)
    
    def check_if_stale(self, element: WebElement, msg: str="") -> bool:
        return check.if_stale(driver=self.driver, element=element, msg=msg)
    
    # find elements in different ways
    def find_by_xpath(self, xpath_list: list[str]):
        return find.by_xpath(driver=self.driver, xpath_list=xpath_list)
    
    def try_click(self, element: WebElement, msg: str="") -> bool:
        return utils.try_click(element=element, timeout=self, msg=msg)
    
    def get_text(self, element: WebElement, msg: str="") -> str:
        return parse.get_text(element=element, timeout=self.wait_timeout, msg=msg)
    