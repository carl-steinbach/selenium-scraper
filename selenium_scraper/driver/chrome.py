import pathlib

import selenium.webdriver
from selenium_stealth import stealth

from selenium_scraper.proxy import manager
from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.user_agent import UserAgent
from selenium_scraper.window import Window

ios_str = ("userAgent=Mozilla/5.0  (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
           "like  Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
android_str = ("Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.0.0 Mobile "
               "Safari/537.36")
android_str_1 = ("Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, "
                 "like Gecko) Version/4.0 Mobile Safari/534.30")


def create_driver(
        user_agent: UserAgent,
        proxy_country: str | None,
        proxy_config: ProxyConfig | None,
        headless: bool,
        window: Window | None,
        enable_stealth: bool,
        user_data_dir: str | None,
        low_data: bool,
        use_undetected_chromedriver: bool
) -> selenium.webdriver.Chrome:
    # preferences
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    if low_data:
        prefs["profile.managed_default_content_settings.images"] = 2

    # options
    if use_undetected_chromedriver:
        # options = undetected_chromedriver.options.ChromeOptions()
        raise Exception("undetected chromedriver is no longer supported")
    else:
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
        proxy_path = proxy_path.joinpath(manager.get_proxy_path(country=proxy_country, config=proxy_config))
        options.add_argument(f"--load-extension={proxy_path.as_posix()}")

    # headless mode
    if headless:
        options.add_argument("--headless=new")

    # user agent
    match user_agent:
        case UserAgent.IOS:
            user_agent_str = '--user-agent=\"' + ios_str + '\"'
            options.add_argument(user_agent_str)
            mobile_emulation = {"deviceName": "iPhone 4"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        case UserAgent.ANDROID:
            user_agent_str = '--user-agent=\"' + android_str + '\"'
            options.add_argument(user_agent_str)
            mobile_emulation = {"deviceName": "Nexus 5"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        case UserAgent.DESKTOP:
            # options.add_argument("--window-size=1920,1080")
            pass

    if use_undetected_chromedriver:
        # driver = undetected_chromedriver.Chrome(headless=headless, options=options)
        raise Exception("undetected-chromedriver is no longer supported")
    else:
        driver = selenium.webdriver.Chrome(options=options)  # desired_capabilities=capabilities)
    if enable_stealth:
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform=_get_platform(user_agent),
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    if user_agent != UserAgent.DESKTOP:
        _set_platform(driver=driver, user_agent=user_agent)
        set_user_agent_data(driver=driver, user_agent=user_agent)

    if window:
        driver.set_window_size(*window.size)
        driver.set_window_position(*window.position)

    return driver


def _set_platform(driver, user_agent):
    source = """
    Object.defineProperty(
        navigator,
        "platform",
        {
            get: function () {
                return "%s";
            },
            set: function (a) {
            }
        }
    );
    """ % (_get_platform(user_agent=user_agent))

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": source})


def _get_platform(user_agent):
    if user_agent == UserAgent.IOS:
        return "iPhone"
    if user_agent == UserAgent.ANDROID:
        return "Android"
    if user_agent == UserAgent.DESKTOP:
        return "MacIntel"


def set_user_agent_data(driver, user_agent):
    match user_agent:
        case UserAgent.IOS:
            mobile = "true"
            platform = "iPhone"
        case UserAgent.ANDROID:
            mobile = "true"
            platform = "Android"
        case _:
            return

    source = """
    Object.defineProperty(
        navigator,
        'userAgentData',
        { 
            get: () => { 
                return {brands: [], mobile: %s, platform: '%s'}
            }
        } 
    )
    """ % (mobile, platform)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": source})
