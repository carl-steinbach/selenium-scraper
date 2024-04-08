import unittest

import selenium_scraper.proxy.manager as proxy_manager
from selenium_scraper.proxy.config import ProxyConfig

proxy_config = ProxyConfig(
    host="localhost",
    port=80, scheme="http",
    locations=["germany", "United-States"],
    username="Username",
    password="Password",
    provider="Packetstream"
)


class ProxyTest(unittest.TestCase):

    def test_invalid_country(self):
        try:
            path = proxy_manager.create_proxy_extension(country="", config=proxy_config)
        except ValueError:
            return

        self.fail(f"Invalid country was not caught. Expected ValueError, got '{path}'")


if __name__ == "__main__":
    unittest.main()
