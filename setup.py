from setuptools import setup, find_packages

setup(
    name="selenium-scraper",
    version="1.5",
    packages=find_packages(),
    install_requires=[
        "pysocks>=1.7.1",
        "seleniumbase>=4.25.4"
    ]
)
