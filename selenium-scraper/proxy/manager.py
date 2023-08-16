import os
import json
import zipfile

proxy_dir = os.path.dirname(os.path.abspath(__file__))
zip_mode = zipfile.ZIP_DEFLATED


def get(country: str) -> str:
    # check if proxy is available
    if country not in scraper.config.proxy.countries:
        raise ValueError(f"proxy is unavailable in this country; got {country}")
    
    if country not in os.listdir(proxy_dir):
        _create_zip(country=country)

    return os.path.join(proxy_dir, country)


def _create_zip(country: str):
    proxy_zip_path = os.path.join(proxy_dir, country, "proxy.zip")

    if os.path.exists(proxy_zip_path):
        return proxy_zip_path
    
    country_pass = scraper.config.proxy.password + f"-{country}"

    manifest_path = os.path.join(proxy_dir, country, "manifest.json")
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
        "minimum_chrome_version":"22.0.0"
    }


    background_path = os.path.join(proxy_dir, country, "background.js")
    background = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "{config.proxy.scheme}",
            host: "{config.proxy.host}",
            port: parseInt("{config.proxy.port}")
        },
        bypassList: ["foobar.com"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "{config.proxy.username}",
                password: "{country_pass}}"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );"""
    
    os.mkdir(os.path.join(proxy_dir, country))
    # write manifest.json and background.js files
    with open(manifest_path, mode="w+") as f:
        json.dump(manifest, f, indent=4)

    with open(background_path, mode="w+") as f:
        f.write(background)
    
    # compress to zip
    with zipfile.ZipFile(proxy_zip_path, mode="w+", compression=zip_mode) as zip:
        zip.write(manifest_path, "manifest", compress_type=zip_mode)
        zip.write(background_path, "background", compress_type=zip_mode)
    
    return proxy_zip_path


if __name__ == "__main__":
    print("create proxy")
    get("Germany")