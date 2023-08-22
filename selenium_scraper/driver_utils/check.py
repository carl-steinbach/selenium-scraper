from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium_scraper.driver_utils import wait
import time


def if_exists(driver: Chrome, locator: tuple, timeout: float) -> WebElement:
    start = time.time()
    while time.time() - start > timeout:
        try:
            return driver.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.1)

    return None


def if_exists_parent(parent: WebElement, locator: tuple, timeout: float) -> WebElement:
    start = time.time()
    while time.time() - start < timeout:
        try:
            return parent.find_element(*locator)
        except NoSuchElementException:
            time.sleep(0.0)

    return None


def if_attribute_exists(element: WebElement, attribute: str) -> bool:
    try:
        if element.get_attribute(attribute) != None:
            return True
    except:
        return False

    return False


def if_alert_exists(driver: Chrome, timeout: float, msg: str) -> bool:
    try:
        return WebDriverWait(driver, timeout).until(
            EC.alert_is_present(), message="check if alert exists" + msg
        )
    except:
        return False


def if_stale(driver: Chrome, element: WebElement, msg: str) -> bool:
    try:
        wait.until_stale(driver=driver, element=element,
                         timeout=0.1, msg="check if stale: " + msg)
        return True
    except:
        return False
