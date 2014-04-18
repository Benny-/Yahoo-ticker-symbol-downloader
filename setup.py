#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'Yahoo-ticker-downloader',
    version = '0.2.8',
    author = 'Benny',
    author_email = 'Benny@GMX.it',
    url='https://github.com/Benny-/Yahoo-ticker-symbol-downloader',
    license='Public Domain',
    keywords = "market finance yahoo ticker stocks etf future index mutualfund currency".split(),
    description='A web scraper for ticker symbols from yahoo finance',
    long_description = open('README.rst').read(),
    packages = find_packages(),
    scripts = ['YahooTickerDownloader.py'],
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
        "requests >= 2.2.1",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: Public Domain",
    ],
)

