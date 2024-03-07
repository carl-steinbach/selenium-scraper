import random
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def until_clickable(driver: Chrome, element: WebElement, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable(element), message="wait until clickable: " + msg
    )


def until_exists(driver: Chrome, locator: tuple, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located(locator),
        message="wait_until_exists: " + msg,
    )


def until_exists_parent(parent: WebElement, locator: tuple, timeout: float, msg: str) -> WebElement:
    start = time.time()
    while time.time() - start < timeout:
        try:
            return parent.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.1)

    raise TimeoutException("wait until exists: " + msg)


def until_exists_list(
        driver: Chrome, locator: tuple, timeout: float, msg: str, number_of_elements: int = 0
) -> list[WebElement]:
    start = time.time()
    while time.time() - start < timeout:
        try:
            elements = driver.find_elements(*locator)
            if elements is not None and len(elements) >= number_of_elements:
                return elements
        except NoSuchElementException:
            time.sleep(0.1)

    raise TimeoutException("wait until exists: " + msg)


def until_exists_list_parent(parent: WebElement, locator: tuple, timeout: float, msg: str,
                             number_of_elements: int = 0) -> list[WebElement]:
    start = time.time()
    while time.time() - start < timeout:
        try:
            elements = parent.find_elements(*locator)
            if elements is not None and len(elements) >= number_of_elements:
                return elements
        except NoSuchElementException:
            time.sleep(0.1)

    raise TimeoutException("wait until exists: " + msg)


def until_invisible(driver: Chrome, element: WebElement, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(
        expected_conditions.invisibility_of_element(element),
        message="wait until invisible: " + msg,
    )


def until_stale(driver: Chrome, element: WebElement, timeout: float, msg: str) -> WebElement:
    return WebDriverWait(driver, timeout).until(expected_conditions.staleness_of(element),
                                                message="wait until stale: " + msg)


def until_not_exists(driver: Chrome, locator: tuple, timeout: float, msg: str) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            driver.find_element(*locator)
        except NoSuchElementException:
            return True

    raise TimeoutException(msg="wait until gone: " + msg)


def random_wait(min_timeout: float, max_timeout: float):
    timeout = random.random() * (max_timeout - min_timeout)
    time.sleep(timeout + min_timeout)
