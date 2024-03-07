import time

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement


def try_click(element: WebElement, timeout: float, msg: str):
    start = time.time()
    while time.time() - start < timeout:
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            time.sleep(0.1)

    raise TimeoutException(msg="try click" + msg)
