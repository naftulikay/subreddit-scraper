# TODO

 * Examine how Scrapy does the item pipeline. As new items are yielded by the scraper, we'd like
   to simply store them without fuss to SQLite as soon as possible to avoid leaking memory.
 * Unit test the request method of the SubredditSpider
 * Write the methods and test methods for get_posts(before) and get_comments(before).
 * Add SQLite library requirements to setup.py.
