import os
import json
import zipfile
from selenium_scraper.config import config


proxy_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions")
zip_mode = zipfile.ZIP_DEFLATED


def get(country: str) -> str:
    # create proxy dir if not exists
    if not os.path.isdir(proxy_dir):
        os.mkdir(proxy_dir)

    # check if proxy is available
    if country not in config.proxy.countries:
        raise ValueError(
            f"proxy is unavailable in this country; got {country}")

    return _create_zip(country=country)


def _create_zip(country: str):
    # create the chrome extension zip
    proxy_zip_path = os.path.join(proxy_dir, country, "proxy.zip")
    country_pass = config.proxy.password + "_country-" + country

    manifest_name = "manifest.json"
    manifest_path = os.path.join(proxy_dir, country, manifest_name)
    manifest = {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }

    background_name = "background.js"
    background_path = os.path.join(proxy_dir, country, background_name)
    background = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "%s",
            host: "%s",
            port: parseInt("%s")
        },
        bypassList: ["foobar.com"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );""" % (config.proxy.scheme, config.proxy.host, config.proxy.port, config.proxy.username, country_pass)

    if not os.path.isdir(os.path.join(proxy_dir, country)):
        os.mkdir(os.path.join(proxy_dir, country))
    # write manifest.json and background.js files
    with open(manifest_path, mode="w+") as f:
        json.dump(manifest, f, indent=4)

    with open(background_path, mode="w+") as f:
        f.write(background)

    # compress to zip
    with zipfile.ZipFile(proxy_zip_path, mode="w", compression=zip_mode) as zip:
        zip.write(manifest_path, "manifest.json", compress_type=zip_mode)
        zip.write(background_path, "background.js", compress_type=zip_mode)

    return proxy_zip_path
