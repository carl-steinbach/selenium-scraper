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
        scraper.driver.get("https://www.primeopinion.com/en-gb")
        scraper.driver.save_screenshot("getting_started_screenshot.png")
        input("press any key to exit")
    finally:
        scraper.quit()
