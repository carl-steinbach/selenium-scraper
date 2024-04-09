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
        proxy_country=None,
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
