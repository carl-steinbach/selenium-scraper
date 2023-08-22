from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random


def until_clickable(driver: Chrome, element: WebElement, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(element), message="wait until clickable: " + msg
    )


def until_exists(driver: Chrome, locator: tuple, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator),
        message="wait_until_exists: " + msg,
    )


def until_exists(parent: WebElement, locator: tuple, timeout: float, msg: str) -> WebElement:
    start = time.time()
    while time.time() - start < timeout:
        try:
            return parent.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.1)

    raise TimeoutException("wait until exists: " + msg)


def until_exists(driver: Chrome or WebElement, locator: tuple, timeout: float, msg: str, number_of_elements: int) -> list(WebElement):
    start = time.time()
    while time.time() - start < timeout:
        try:
            list = driver.find_elements(*locator)
            if list is not None and len(list) >= number_of_elements:
                return list
        except NoSuchElementException:
            time.sleep(0.1)

    raise TimeoutException("wait until exists: " + msg)


def until_invisible(driver: Chrome, locator: tuple, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located(locator),
        message="wait until invisible: " + msg,
    )


def until_stale(driver: Chrome, element: WebElement, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(EC.staleness_of(element), message="wait until stale: " + msg)


def until_not_exists(driver: Chrome, locator: tuple, timeout: float, msg: str) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            driver.find_element(*locator)
        except NoSuchElementException:
            return True

    raise TimeoutException(msg="wait until gone: " + msg)


def until_not_exists(parent: WebElement, locator: tuple, timeout: float, msg: str) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            parent.find_element(*locator)
        except NoSuchElementException:
            return True

    raise TimeoutException(msg="wait until gone: " + msg)


def random_wait(min_timeout: float, max_timeout: float):
    timeout = random.random() * (max_timeout - min_timeout)
    time.sleep(timeout + min_timeout)




