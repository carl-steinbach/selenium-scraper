import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement


def until_loaded(driver: Chrome, body: WebElement, locator: tuple, timeout: float, msg: str):
    """scroll down until an element is loaded"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            return driver.find_element(*locator)
        except NoSuchElementException:
            driver.execute_script('arguments[0].scrollTop += 100', body)

    raise TimeoutException(msg="scroll_until_loaded: " + msg)


def into_view(driver: Chrome, body: WebElement, element: WebElement, window_height: int):
    viewport_distance = driver.execute_script("return arguments[0].getBoundingClientRect().top", element)
    driver.execute_script("arguments[0].scrollTop += arguments[1]", body, viewport_distance - window_height / 2)


def until_timeout(driver: Chrome, body: WebElement, timeout: float):
    start = time.time()
    while time.time() - start < timeout:
        driver.execute_script('arguments[0].scrollTop += 100', body)
