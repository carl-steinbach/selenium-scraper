import os
import unittest

import selenium_scraper.proxy.manager as proxy_manager
from selenium_scraper.proxy.config import ProxyConfig

proxy_config = ProxyConfig(
    host="localhost",
    port=80, scheme="http",
    locations=["germany", "united-states"],
    username="Username",
    password="Password",
    provider="Packetstream"
)


class ProxyTest(unittest.TestCase):
    def test_create_proxy(self):
        proxy_path = proxy_manager.get_proxy_path(country="united-states", config=proxy_config)
        self.assertTrue(os.path.isfile(proxy_path))

    def test_invalid_country(self):
        try:
            path = proxy_manager.get_proxy_path(country="", config=proxy_config)
        except ValueError:
            return

        self.fail(f"Invalid country was not caught. Expected ValueError, got '{path}'")


if __name__ == "__main__":
    unittest.main()
