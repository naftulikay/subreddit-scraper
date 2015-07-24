#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "redditsubscraper",
    version = "0.0.1",
    packages = find_packages('src'),
    package_dir = { '': 'src'},
    install_requires = ['setuptools',
        'scrapy >= 1.0.1, < 1.1.0',
        'basehash',
    ],
    entry_points = {
        'console_scripts': [
            'reddit-sub-scraper = redditsubscraper.cli:main'
        ]
    }
)
