import time

import selenium_scraper.scraper

if __name__ == "__main__":
    scraper = selenium_scraper.scraper.Scraper(
        name="test",
        proxy=None,  # "USER:PASS@SERVER:PORT"
        undetected=False,
        headless=False,
        user_data_dir=None
    )
    scraper.start()
    try:
        scraper.driver.get("https://google.com")
        time.sleep(10)
        scraper.driver.save_screenshot("getting_started_screenshot.png")
    finally:
        scraper.quit()
