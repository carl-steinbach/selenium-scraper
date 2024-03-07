import time

from selenium_scraper.driver import chrome
from selenium_scraper.user_agent import UserAgent

if __name__ == "__main__":
    driver = chrome.create_driver(
        user_agent=UserAgent.DESKTOP,
        proxy_country=None,
        proxy_config=None,
        headless=False,
        window=None,
        enable_stealth=True,
        user_data_dir=None,
        low_data=False,
        use_undetected_chromedriver=True
    )

    try:
        driver.get('nowsecure.nl')
        driver.save_screenshot('nowsecure.png')
        time.sleep(600)
    finally:
        driver.quit()
