#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = 'Yahoo-ticker-downloader',
	version = '0.1.1',
	author = 'Benny',
	author_email = 'Benny@GMX.it',
	url='https://github.com/Benny-/Yahoo-ticker-symbol-downloader',
	license='LICENSE.txt',
	description='A python3 script to scrape a lot - but not all - ticker symbols from yahoo finance',
	packages = find_packages(),
	scripts = ['YahooTickerDownloader.py'],
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
    ],
)

