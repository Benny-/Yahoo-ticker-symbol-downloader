#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = 'Yahoo ticker downloader',
	version = '0.1.0',
	packages = find_packages(),
	scripts = ['YahooTickerDownloader.py'],
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
    ],
)

