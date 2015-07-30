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
    parser.add_argument('-o', '--output-dir', required=True,
        help="The directory to save posts to.")
    parser.add_argument('subreddit', nargs=1,
        help="The name of the subreddits you wish to download.")

    args = parser.parse_args()

    # configure basic logging; for every time -v is passed, deduct 10 from WARNING,
    # allowing no further than 0.
    logging.basicConfig(level=max(logging.WARNING - (len(args.verbosity) * 10), 0),
        format="[%(levelname)s] %(message)s")

    logging.debug("Program Arguments: %s", args)

    # create the output directory if not present
    if not os.path.isdir(args.output_dir):
        try:
            logger.debug("Output dir %s is not present, making directory/directories.",
                args.output_dir)
            os.makedirs(args.output_dir)
        except OSError as e:
            logger.error('Unable to create the output directory %s: %s', args.output_dir,
                e)
            sys.exit(1)

    # attempt to make a directory for the subs entries
    sub_output_dir = os.path.join(args.output_dir, args.subreddit)

    if not os.path.isdir(sub_output_dir):
        try:
            logger.debug("Subreddit output dir %s not present, creating it now.",
                sub_output_dir)
            os.makedirs(sub_output_dir)
        except OSError as e:
            logger.error('Unable to create the subreddit output directory %s: %s',
                sub_output_dir, e)
            sys.exit(1)

    # okay, now do the actual indexing
    logger.info("Running crawler for the %s subreddit.", subreddit)

    # instantiate the crawler process
    process = scrapy.crawler.CrawlerProcess({
        'BOT_NAME': 'subreddit-scraper-0.0.1',
        'DOWNLOAD_DELAY': 2, # seconds I hope
        'RANDOMIZE_DOWNLOAD_DELAY': False, # no thanks bro
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1, # reddit hates
    })

    process.crawl(SubredditSpider, subreddit_name=args.subreddit)
    process.start()

if __name__ == "__main__":
    main()
