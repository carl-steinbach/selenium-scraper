from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome

def by_xpath(driver: Chrome, xpath_list: list[str]) -> WebElement:
    xpath = ""
    for xpath_part in xpath_list:
        xpath += xpath_part
        try:
            result = driver.find_element(By.XPATH, xpath)
        except:
            print(f"could not find {xpath_list}")
            return None
    
    return result



