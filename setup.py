from setuptools import setup

setup(
    name="selenium-scraper",
    version="1.5",
    packages=["selenium_scraper"],
    install_requires=[
        "pysocks>=1.7.1",
        "seleniumbase>=4.25.4"
    ]
)
