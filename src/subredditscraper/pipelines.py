#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

class SQLiteItemPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_file = crawler.settings.get('DATABASE_FILE', 'subreddits.db'),
        )

    def __init__(self, database_file):
        """
        Constructor for the SQLiteItemPipeline.

        Arguments:
        database_file: The path to the database file to write to.
        """
        self.database_file = database_file


    def open_spider(self, spider):
        """
        Callback method triggered on start of the spider.

        Arguments:
        spider: The spider instance which is opening this pipeline.
        """
        # TODO determine if tables exist in the database and create if necessary
        pass

    def close_spider(self, spider):
        """
        Callback method triggered on finish of the spider.

        Arguments:
        spider: The spider instance which has finished with this pipeline.
        """
        pass

    def process_item(self, item, spider):
        """
        Callback method triggered for each item recovered from the spider.

        Arguments:
        item: The item produced by the spider.
        spider: The spider which produced the item.
        """
        # TODO create a connection object to the database file for every single item (because sqlite hates threads)
        # TODO select count(*) from [links|comments] where id = ?; if > 0, update, else insert
        pass
