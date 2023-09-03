import os
import json
import zipfile
from selenium_scraper.proxy.config import ProxyConfig
from selenium_scraper.proxy.providers import packetstream


proxy_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions")
zip_mode = zipfile.ZIP_DEFLATED
available_providers = ["packetstream"]


# create the proxy extension and return the path
def get_proxy_path(country: str, config: ProxyConfig) -> str:
    if not os.path.isdir(proxy_dir):
        os.mkdir(proxy_dir)

    if country not in config.locations:
        raise ValueError(
            f"proxy is unavailable in this country; got {country}")
    
    match str(config.provider).lower():
        case "packetstream":
            return packetstream.create_zip(country=country, config=config)
        case _:
            raise ValueError("No zip method available for this provider")

