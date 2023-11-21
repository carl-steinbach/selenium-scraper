import json
import os
import zipfile

from selenium_scraper.proxy.config import ProxyConfig


# Create the Chrome extension zip file
def create_zip(country: str, config: ProxyConfig, proxy_dir: str):
    formatted_country = country.replace("-", "")
    zip_mode = zipfile.ZIP_DEFLATED
    proxy_zip_path = os.path.join(proxy_dir, formatted_country, "proxy.zip")
    country_pass = config.password + "_country-" + formatted_country

    manifest_name = "manifest.json"
    manifest_path = os.path.join(proxy_dir, formatted_country, manifest_name)
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
    background_path = os.path.join(proxy_dir, formatted_country, background_name)
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
    );""" % (config.scheme, config.host, config.port, config.username, country_pass)

    if not os.path.isdir(os.path.join(proxy_dir, formatted_country)):
        os.mkdir(os.path.join(proxy_dir, formatted_country))
    # write manifest.json and background.js files
    with open(manifest_path, mode="w+") as f:
        json.dump(manifest, f, indent=4)

    with open(background_path, mode="w+") as f:
        f.write(background)

    # compress to zip
    with zipfile.ZipFile(proxy_zip_path, mode="w", compression=zip_mode) as extension_zip:
        extension_zip.write(manifest_path, "manifest.json", compress_type=zip_mode)
        extension_zip.write(background_path, "background.js", compress_type=zip_mode)

    return formatted_country
