#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sqlite3


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


    def save_link(self, link):
        """
        Insert a new row into the links table, storing the link.
        """
        pass

    def update_link(self, link):
        """
        Update an existing row in the database with the given link information.
        """
        pass


    def link_exists(self, link):
        """
        Evaluates whether a link exists in the database. Use this method to determine whether to insert or update
        a link in the database.
        """
        pass


    def new_connection(self):
        """
        Factory method for creating a new connection to the SQLite database.

        Returns:
        A properly configured SQLite connection object.
        """
        result = sqlite3.connect(self.database_file)
        result.row_factory = sqlite3.Row

        return result


    def get_table_names(self, connection):
        """
        Returns a list of the table names present in the SQLite database.

        Arguments:
        connection: SQLite connectioon to the database.

        Returns:
        A list containing string names of the tables present in the database.
        """
        with connection:
            return [i[0] for i in connection.execute('select name from sqlite_master where type="table";')]


    def tables_exist(self, connection):
        """
        Determines whether the required SQL tables exist.

        Arguments:
        connection: SQLite connection to the database.

        Returns:
        True if the tables exist, False otherwise.
        """
        table_names = self.get_table_names(connection)

        if 'links' in table_names and 'comments' in table_names:
            return True
        else:
            return False

    def create_tables(self, connection):
        """
        Creates the database tables for links and comments. If database tables previously exist in the database,
        they'll be dropped and recreated by this method. Only call this method if you understand the implications.

        Arguments:
        connection: SQLite connection to the database.
        """
        with connection:
            # drop links if it exists
            connection.execute('drop table if exists links;')
            # create links table
            connection.execute(
                "create table links ("
                "    id text primary key,"
                "    created integer,"
                "    created_utc integer,"
                "    ups integer,"
                "    downs integer,"
                "    likes integer,"
                "    prefixed_id text,"
                "    author text,"
                "    author_flair_css_class text,"
                "    author_flair_text text,"
                "    clicked integer,"
                "    domain text,"
                "    hidden integer,"
                "    is_self integer,"
                "    link_flair_css_class text,"
                "    link_flair_text text,"
                "    media text,"
                "    media_embed text,"
                "    num_comments integer,"
                "    over_18 integer,"
                "    permalink text,"
                "    saved integer,"
                "    score integer,"
                "    selftext text,"
                "    selftext_html text,"
                "    subreddit text,"
                "    subreddit_id text,"
                "    thumbnail text,"
                "    title text,"
                "    url text,"
                "    edited integer,"
                "    distinguished text,"
                "    stickied integer"
                ");"
            )
            # drop comments if it exists
            connection.execute('drop table if exists comments;')
            # create comments table
            connection.execute(
                "create table comments ("
                "    id text primary key,"
                "    created integer,"
                "    created_utc integer,"
                "    ups integer,"
                "    downs integer,"
                "    likes integer,"
                "    prefixed_id text,"
                "    approved_by text,"
                "    author text,"
                "    author_flair_css_class text,"
                "    author_flair_text text,"
                "    banned_by text,"
                "    body text, "
                "    body_html text,"
                "    edited integer,"
                "    gilded integer,"
                "    link_author text,"
                "    link_id text,"
                "    link_title text,"
                "    link_url text,"
                "    num_reports integer,"
                "    parent_id text,"
                "    saved integer,"
                "    score integer,"
                "    score_hidden integer,"
                "    subreddit text,"
                "    subreddit_id text,"
                "    distinguished text"
                ");"
            )


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
