import os

from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.proxy.providers import packetstream

proxy_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions")
available_providers = ["packetstream"]


# create the proxy extension and return the path
def create_proxy_extension(country: str, config: ProxyConfig) -> str:
    """returns the path to the proxy directory relative to the extensions directory"""
    if not os.path.isdir(proxy_dir):
        os.mkdir(proxy_dir)

    if country not in config.locations or country is None or country == "":
        raise ValueError(
            f"proxy is unavailable in this country, got {country}")

    match str(config.provider).lower():
        case "packetstream":
            return packetstream.create_zip(country=country, config=config, proxy_dir=proxy_dir)
        case _:
            raise ValueError("No zip method available for this provider")
