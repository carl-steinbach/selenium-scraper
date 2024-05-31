# Selenium Web Scraper

This package provides a wrapper for the [Selenium Web Driver](https://www.selenium.dev) to facilitate web scraping. Adds various utiliy methods to access elements on the 
page, capture redirects and navigate pages. Uses the [SeleniumBase](https://seleniumbase.io) package to create the driver.

## Installation

Install via pip using 

`pip install git+https://github.com/carl-steinbach/selenium-scraper.git`

## Getting started

Create a scraper by instantiating the `selenium_scraper.scraper.Scraper` class, and example instantiation can be viewed 
in the `getting_started.py` module. 

Calling `start()` on the scraper will start a chromedriver instance, the `driver` attribute can be used to
directly access the chromedriver. Ensure to call `quit()` after use, this will also close associated virtual 
displays.

In order to use a proxy, pass a proxy string formatted like so `"USER:PASS@SERVER:PORT"`.

```
# from getting_started.py
import selenium_scraper.scraper
import sbvirtualdisplay

USE_VIRTUAL_DISPLAY = False

if __name__ == "__main__":
    if USE_VIRTUAL_DISPLAY:
        # if you want to use a virtual display, configure it like so:
        display = sbvirtualdisplay.Display(visible=True, size=(1440, 1880))
    else:
        display = None


    scraper = selenium_scraper.scraper.Scraper(
        name="test",
        proxy=None,  # "USER:PASS@SERVER:PORT"
        undetected=False,
        headless=False,
        virtual_display=display,
        user_data_dir=None
    )
    scraper.start(devtools=True)
    try:
        scraper.driver.get("https://ipinfo.io")
        scraper.driver.save_screenshot("getting_started_screenshot.png")
        input("press any key to exit")
    finally:
        scraper.quit()
```



---

Author:  Carl Steinbach

Version: 1.7

---
