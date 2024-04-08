# Selenium Web Scraper

A wrapper for the Selenium web driver to facilitate web scraping. Hides some automation headers and provides support for
adding a proxy. The `selenium-stealth` package can optionally be used to further obfuscate the driver using the
`enable_stealth` param.

## Installation

Install via pip using 

`pip install git+https://github.com/carl-steinbach/selenium-scraper.git`

Example instantiation of the Scraper class can be seen in the `selenium_scraper.scraper.Scraper.py` module.

## Getting started

Start an instance of the driver by instantiating the `selenium_scraper.scraper.Scraper` class.
Calling the `start()` method of the scraper will start a chromedriver instance, the `driver` parameter can be used to
directly access the chromedriver.

In order to use a proxy, add your credentials to the ProxyConfig object and pass it to the scraper constructor.

```
import selenium_scraper.proxy.config
import selenium_scraper.scraper
import selenium_scraper.user_agent

proxy_config = selenium_scraper.proxy.config.ProxyConfig(
    host="<PROXY_HOST>",
    port="<PROXY_PORT>",
    scheme="https",
    locations=["United-States", "Germany"],  # these values are used to validate the `proxy_country` attribute
    username="<USERNAME>",
    password="<PASSWORD>",
    provider="packetstream"  # only packet stream is implemented right now
)

if __name__ == "__main__":
    scraper = selenium_scraper.scraper.Scraper(
        name="test",
        user_agent=selenium_scraper.user_agent.UserAgent.DESKTOP,
        proxy_config=None,
        proxy_country="United-States",
        headless=True,
        verbose=True,
        dry_run=True,
        window=None,
        enable_stealth=True,
        user_data_dir=None,
        low_data=False
    )
    try:
        scraper.start()
        scraper.driver.get("https://google.com")
        scraper.driver.save_screenshot("getting_started_screenshot.png")
    finally:
        scraper.quit()
```



---

Author:  Carl Steinbach

Version: 1.3

---
