# Selenium Web Scraper

A wrapper for the Selenium web driver to facilitate web scraping. Hides some automation headers and provides support for
adding a proxy. The `selenium-stealth` package can optionally be used to further obfuscate the driver using the
`enable_stealth` param.

## Installation

Install via pip using `pip install git+https://{$token}@github.com/carl-steinbach/selenium-scraper.git`

Example instantiation of the Scraper class can be seen in the `selenium_scraper.scraper.Scraper.py` module.

## Startup

Start an instance of the driver by instantiating the `selenium_scraper.scraper.Scraper` class.
Calling the `start()` method of the scraper will start a chromedriver instance, the `driver` parameter can be used to
directly access the chromedriver.

---

Author:  Carl Steinbach

Version: 1.3

---
