#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

logger = logging.getLogger('redditsubscraper.cli')

def main():
    parser = argparse.ArgumentParser(prog='reddit-sub-scraper',
        description="A utility for downloading a subreddit's posts and comments.")
    parser.add_argument('-o', '--output-dir', required=True,
        help="The directory to save posts to.")
    parser.add_argument('subreddit', nargs='+',
        help="The name(s) of the subreddits you wish to download.")

    args = parser.parse_args()

    # configure basic logging
    logging.basicConfig(level=logging.WARNING, format="[%(levelname)s] %(message)s")

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

    for subreddit in args.subreddit:
        # attempt to make a directory for the subs entries
        sub_output_dir = os.path.join(args.output_dir, subreddit)

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


if __name__ == "__main__":
    main()
