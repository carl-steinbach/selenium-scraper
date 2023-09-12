from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def by_xpath(driver: Chrome, xpath_list: list[str], verbose: bool) -> WebElement | None:
    xpath = ""
    result = None
    for xpath_part in xpath_list:
        xpath += xpath_part
        try:
            result = driver.find_element(By.XPATH, xpath)
        except Exception:
            if verbose:
                print(f"could not find {xpath_list}")
            return None

    return result
