#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import scrapy
import sys

from scrapy.process import CrawlerProcess
from subredditscraper.spiders import SubredditSpider

logger = logging.getLogger('subredditscraper.cli')

def main():
    parser = argparse.ArgumentParser(prog='reddit-sub-scraper',
        description="A utility for downloading a subreddit's posts and comments.")
    parser.add_argument('-v', action='append_const', dest='verbosity', const=True,
        help="Set verboseness. Pass once for info-level logs, twice for debug-level logs.")
    parser.add_argument('-d', '--database-file', default="subreddits.db",
        help="The database file to save posts to.")
    parser.add_argument('subreddit', nargs=1,
        help="The name of the subreddits you wish to download.")

    args = parser.parse_args()

    # configure basic logging; for every time -v is passed, deduct 10 from WARNING,
    # allowing no further than 0.
    logging.basicConfig(level=max(logging.WARNING - (len(args.verbosity) * 10), 0),
        format="[%(levelname)s] %(message)s")

    logging.debug("Program Arguments: %s", args)

    # okay, now do the actual indexing
    logger.info("Running crawler for the %s subreddit.", subreddit)

    # instantiate the crawler process
    process = scrapy.crawler.CrawlerProcess({
        'BOT_NAME': 'subreddit-scraper-0.0.1',
        'DOWNLOAD_DELAY': 2, # seconds I hope
        'RANDOMIZE_DOWNLOAD_DELAY': False, # no thanks bro
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1, # reddit hates,
        'DATABASE_FILE': args.database_file,
        'ITEM_PIPELINES': {
            'subredditscraper.pipelines.SQLiteItemPipeline': 100,
        }
    })

    process.crawl(SubredditSpider, subreddit_name=args.subreddit)
    process.start()

if __name__ == "__main__":
    main()
