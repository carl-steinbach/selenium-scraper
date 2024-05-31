from setuptools import setup, find_packages

setup(
    name="selenium-scraper",
    version="1.7",
    packages=find_packages(),
    install_requires=[
        "seleniumbase>=4.25.4"
    ]
)
