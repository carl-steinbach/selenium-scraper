import logging
import pathlib

import selenium.webdriver

from selenium_scraper.proxy import manager
from selenium_scraper.proxy.config import ProxyConfig

logger = logging.getLogger(__name__)


def create_driver(
        proxy_country: str | None,
        proxy_config: ProxyConfig | None,
        headless: bool,
        user_data_dir: str | None,
        low_data: bool
) -> selenium.webdriver.Chrome:
    # preferences
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    if low_data:
        prefs["profile.managed_default_content_settings.images"] = 2

    # options
    options = selenium.webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_experimental_option("prefs", prefs)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--enable-logging --v=1")
    options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

    if user_data_dir:
        options.add_argument(f"--user-data-dir={user_data_dir}")

    # add proxy
    if proxy_country and proxy_config:
        # options.add_extension(manager.get_proxy_path(country=proxy_country, config=proxy_config))
        proxy_path = pathlib.Path(__file__).parent.parent.resolve().joinpath("proxy", "extensions")
        proxy_path = proxy_path.joinpath(manager.create_proxy_extension(country=proxy_country, config=proxy_config))
        options.add_argument(f"--load-extension={proxy_path.as_posix()}")
        logger.info(f"loaded proxy for {proxy_country}")

    # headless mode
    if headless:
        options.add_argument("--headless=new")

    driver = selenium.webdriver.Chrome(options=options)  # desired_capabilities=capabilities)

    return driver
