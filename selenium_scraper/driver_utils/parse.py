from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException
from time import sleep, time
import re as regex


def get_text(element, timeout=60.0, msg=""):
    start = time()
    while element.text == "":
        if time() - start > timeout:
            raise TimeoutException(msg="get_text: " + msg)

    return element.text


