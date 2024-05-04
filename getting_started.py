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
    scraper.start(devtools=True)
    try:
        scraper.driver.get("https://google.com")
        scraper.driver.save_screenshot("getting_started_screenshot.png")
        input("press any key to exit")
    finally:
        scraper.quit()
