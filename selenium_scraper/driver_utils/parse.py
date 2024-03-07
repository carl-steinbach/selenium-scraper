from time import time

from selenium.common.exceptions import TimeoutException


def get_text(element, timeout=60.0, msg=""):
    start = time()
    while element.text == "":
        if time() - start > timeout:
            raise TimeoutException(msg="get_text: " + msg)

    return element.text
