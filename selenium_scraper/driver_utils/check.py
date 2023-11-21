import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from selenium_scraper.driver_utils import wait


def if_exists(driver: Chrome, locator: tuple, timeout: float) -> WebElement | None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            return driver.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.1)

    return None


def if_exists_parent(parent: WebElement, locator: tuple, timeout: float) -> WebElement | None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            return parent.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.1)

    return None


def if_attribute_exists(element: WebElement, attribute: str) -> str | None:
    try:
        return element.get_attribute(attribute)
    except Exception:
        return None


def if_alert_exists(driver: Chrome, timeout: float, msg: str) -> Alert | None:
    try:
        return WebDriverWait(driver, timeout).until(
            expected_conditions.alert_is_present(), message="check if alert exists" + msg
        )
    except Exception:
        return None


def if_stale(driver: Chrome, element: WebElement, msg: str) -> bool:
    try:
        wait.until_stale(driver=driver, element=element,
                         timeout=0.1, msg="check if stale: " + msg)
        return True
    except Exception:
        return False
