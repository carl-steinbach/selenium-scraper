# Selenium Web Scraper

This package provides a wrapper for the [Selenium Web Driver](https://www.selenium.dev) to facilitate web scraping. Adds various utiliy methods to access elements on the 
page, capture redirects and navigate pages. Uses the [SeleniumBase](https://seleniumbase.io) package to create the driver.

## Installation

Install via pip using 

`pip install git+https://github.com/carl-steinbach/selenium-scraper.git`

Example instantiation of the Scraper class can be seen in the `selenium_scraper.scraper.Scraper.py` module.

## Getting started

Create a scraper by instantiating the `selenium_scraper.scraper.Scraper` class.
Calling the `start()` method of the scraper will start a chromedriver instance, the `driver` attribute can be used to
directly access the chromedriver. Ensure to call the scrapers `quit` method after use.

In order to use a proxy, pass a proxy string formatted like so `"USER:PASS@SERVER:PORT"`.

```
import selenium_scraper.proxy.config
import selenium_scraper.scraper
import selenium_scraper.user_agent

if __name__ == "__main__":
    scraper = selenium_scraper.scraper.Scraper(
        name="test",
        proxy=None, # proxy format "USER:PASS@SERVER:PORT"
        headless=True,
        undetected=False
        user_data_dir=None
    )
    try:
        scraper.start(devtools=True) # pass additional keyword arguments to the seleniumbase Driver constructor here
        scraper.driver.get("https://google.com")
        scraper.driver.save_screenshot("getting_started_screenshot.png")
    finally:
        scraper.quit()
```



---

Author:  Carl Steinbach

Version: 1.7

---
