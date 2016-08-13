#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'Yahoo-ticker-downloader',
    version = '0.8.1',
    author = 'Benny',
    author_email = 'Benny@GMX.it',
    url='https://github.com/Benny-/Yahoo-ticker-symbol-downloader',
    license='BSD3',
    keywords = "market finance yahoo ticker stock stocks etf future futures index mutualfund currency warrant bond bonds".split(),
    description='A web scraper for ticker symbols from yahoo finance',
    long_description = open('README.rst').read(),
    packages = find_packages(),
    scripts = ['YahooTickerDownloader.py'],
    install_requires=[
        "beautifulsoup4 >= 4.2.1",
        "requests >= 2.2.1",
        "tablib >= 0.9.11",
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: BSD License",
    ],
)

