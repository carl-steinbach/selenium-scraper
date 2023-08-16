import unittest
import selenium_scraper.proxy.manager as proxy_manager
import os


class ProxyTest(unittest.TestCase):
    def test_create_proxy(self):
        proxy_path = proxy_manager.get("Germany")
        self.assertTrue(os.path.isfile(proxy_path))

    def test_invalid_country(self):
        try:
            path = proxy_manager.get("")
        except ValueError:
            return
        
        self.fail(f"Invalid country was not caught. Expected ValueError, got '{path}'")


if __name__ == "__main__":
    unittest.main()

