#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import sqlite3
import tempfile
import unittest

from subredditscraper.exceptions import InvalidIdException

from subredditscraper.items import (
    bool_serializer,
    edited_serializer,
    id_serializer,
    link_id_serializer,
    comment_id_serializer,
    time_serializer,
)

from subredditscraper.pipelines import SQLiteItemPipeline

from subredditscraper.spiders import SubredditSpider


class SQLiteItemPipelineTestCase(unittest.TestCase):
    """
    Test cases for the SQLite item pipeline.
    """

    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        self.connection.row_factory = sqlite3.Row


    def tearDown(self):
        self.connection.close()


    def test_get_table_names(self):
        """
        Tests that the get table names function returns a list of table names present in the database.
        """
        reference = SQLiteItemPipeline(':memory:')

        self.assertEquals([], reference.get_table_names(self.connection))

        with self.connection:
            self.connection.execute('create table llamas (id integer primary key);')

        self.assertEquals(['llamas'], reference.get_table_names(self.connection))


    def test_create_tables(self):
        """
        Tests that creation of the database tables works as expected.
        """
        reference = SQLiteItemPipeline(':memory:')

        with self.connection:
            # no tables to start with
            self.assertEqual(0, len([i[0] for i in self.connection.execute('select name from sqlite_master where type="table";')]))

        # create the tables nao
        reference.create_tables(self.connection)

        with self.connection:
            tables = [i['name'] for i in self.connection.execute('select name from sqlite_master where type="table";')]

        # determine that tables have been created
        self.assertTrue('links' in tables)
        self.assertTrue('comments' in tables)

        # determine that links columns exist
        with self.connection:
            links_columns = {i['name']: i['type'] for i in self.connection.execute('pragma table_info(links);')}

        # TODO test the types of each column for accuracy
        self.assertIn('id', links_columns.keys())
        self.assertIn('created', links_columns.keys())
        self.assertIn('created_utc', links_columns.keys())
        self.assertIn('ups', links_columns.keys())
        self.assertIn('downs', links_columns.keys())
        self.assertIn('likes', links_columns.keys())
        self.assertIn('prefixed_id', links_columns.keys())
        self.assertIn('author', links_columns.keys())
        self.assertIn('author_flair_css_class', links_columns.keys())
        self.assertIn('author_flair_text', links_columns.keys())
        self.assertIn('clicked', links_columns.keys())
        self.assertIn('domain', links_columns.keys())
        self.assertIn('hidden', links_columns.keys())
        self.assertIn('is_self', links_columns.keys())
        self.assertIn('link_flair_css_class', links_columns.keys())
        self.assertIn('link_flair_text', links_columns.keys())
        self.assertIn('media', links_columns.keys())
        self.assertIn('media_embed', links_columns.keys())
        self.assertIn('num_comments', links_columns.keys())
        self.assertIn('over_18', links_columns.keys())
        self.assertIn('permalink', links_columns.keys())
        self.assertIn('saved', links_columns.keys())
        self.assertIn('score', links_columns.keys())
        self.assertIn('selftext', links_columns.keys())
        self.assertIn('selftext_html', links_columns.keys())
        self.assertIn('subreddit', links_columns.keys())
        self.assertIn('subreddit_id', links_columns.keys())
        self.assertIn('thumbnail', links_columns.keys())
        self.assertIn('title', links_columns.keys())
        self.assertIn('url', links_columns.keys())
        self.assertIn('edited', links_columns.keys())
        self.assertIn('distinguished', links_columns.keys())
        self.assertIn('stickied', links_columns.keys())

        # determine that comments columns exist
        with self.connection:
            comments_columns = {i['name']: i['type'] for i in self.connection.execute('pragma table_info(comments);')}

        # TODO test the types of each column for accuracy
        self.assertIn('id', comments_columns.keys())
        self.assertIn('created', comments_columns.keys())
        self.assertIn('created_utc', comments_columns.keys())
        self.assertIn('ups', comments_columns.keys())
        self.assertIn('downs', comments_columns.keys())
        self.assertIn('likes', comments_columns.keys())
        self.assertIn('prefixed_id', comments_columns.keys())
        self.assertIn('approved_by', comments_columns.keys())
        self.assertIn('author', comments_columns.keys())
        self.assertIn('author_flair_css_class', comments_columns.keys())
        self.assertIn('author_flair_text', comments_columns.keys())
        self.assertIn('banned_by', comments_columns.keys())
        self.assertIn('body', comments_columns.keys())
        self.assertIn('body_html', comments_columns.keys())
        self.assertIn('edited', comments_columns.keys())
        self.assertIn('gilded', comments_columns.keys())
        self.assertIn('link_author', comments_columns.keys())
        self.assertIn('link_id', comments_columns.keys())
        self.assertIn('link_title', comments_columns.keys())
        self.assertIn('link_url', comments_columns.keys())
        self.assertIn('num_reports', comments_columns.keys())
        self.assertIn('parent_id', comments_columns.keys())
        self.assertIn('saved', comments_columns.keys())
        self.assertIn('score', comments_columns.keys())
        self.assertIn('score_hidden', comments_columns.keys())
        self.assertIn('subreddit', comments_columns.keys())
        self.assertIn('subreddit_id', comments_columns.keys())
        self.assertIn('distinguished', comments_columns.keys())


    def test_tables_exist(self):
        """
        Determines if the table presence logic works.
        """
        reference = SQLiteItemPipeline(':memory:')

        self.assertFalse(reference.tables_exist(self.connection))

        with self.connection:
            self.connection.execute('create table links (id integer primary key);')

        self.assertFalse(reference.tables_exist(self.connection))

        with self.connection:
            self.connection.execute('create table comments (id integer primary key);')

        self.assertTrue(reference.tables_exist(self.connection))

        with self.connection:
            self.connection.execute('drop table links;')

        self.assertFalse(reference.tables_exist(self.connection))


class ItemsTestCase(unittest.TestCase):
    """
    Test cases for global items.
    """

    def test_bool_serializer(self):
        """
        Tests that the boolean serializer serializes a value to True, False, or None.
        """
        self.assertEqual(None, bool_serializer(None))
        self.assertEqual(True, bool_serializer(True))
        self.assertEqual(False, bool_serializer(False))

    def test_edited_serializer(self):
        """
        Tests that the float or none serializer serializes a value to a float or None.
        """
        # test boolean value
        self.assertEqual(None, edited_serializer(False))
        self.assertEqual(1, edited_serializer(True))
        # test string value
        self.assertEqual(None, edited_serializer('nope'))
        # convert long to float
        self.assertEqual(3, edited_serializer(3L))
        # convert float to float
        self.assertEqual(3, edited_serializer(3.0))
        # convert int to float
        self.assertEqual(3, edited_serializer(3))
        # rounding
        self.assertEqual(4, edited_serializer(3.9))
        self.assertEqual(4, edited_serializer(4.2))


    def test_id_serializer(self):
        """
        Tests that the id serializer removes the prefix from a base-36 id.
        """
        # test for cases which should work
        self.assertEqual('abc123', id_serializer('t1_abc123'))
        self.assertEqual('abc123', id_serializer('abc123'))
        self.assertEqual(u'abc123', id_serializer(u't1_abc123'))

        # test for cases which should not work
        self.assertEqual(None, id_serializer('LOL_NOT_MATCHING'))
        self.assertEqual(None, id_serializer(1))
        self.assertEqual(None, id_serializer(None))

    def test_link_id_serializer(self):
        """
        Tests that the link id serializer works as planned.
        """
        # cases which should work
        self.assertEqual(u't3_abc123', link_id_serializer(u'abc123'))
        self.assertEqual(u't3_abc123', link_id_serializer(u't3_abc123'))
        self.assertEqual('t3_abc123', link_id_serializer('abc123'))

        # cases which should not work
        self.assertEqual(None, link_id_serializer('LOL_NOT_MATCHING'))
        self.assertEqual(None, link_id_serializer(1))
        self.assertEqual(None, link_id_serializer(None))

    def test_comment_id_serializer(self):
        """
        Tests that the comment id serializer works as planned.
        """
        # cases which should work
        self.assertEqual(u't1_abc123', comment_id_serializer(u'abc123'))
        self.assertEqual(u't1_abc123', comment_id_serializer(u't1_abc123'))
        self.assertEqual('t1_abc123', comment_id_serializer('t1_abc123'))

        # cases which should not work
        self.assertEqual(None, comment_id_serializer('LOL_NOT_MATCHING'))
        self.assertEqual(None, comment_id_serializer(1))
        self.assertEqual(None, comment_id_serializer(None))

    def test_time_serializer(self):
        """
        Tests that the time serializer converts a time into the right format.
        """
        self.assertEqual(100, time_serializer(100.0))
        self.assertEqual(100, time_serializer(100.10245))
        self.assertEqual(101, time_serializer(100.5))


class SubredditSpiderTestCase(unittest.TestCase):
    """
    Test cases for the SubredditSpider.
    """

    def test_id_regex(self):
        """
        Test that the id regular expression behaves as expected.
        """
        r = SubredditSpider.id_regex

        all_inclusive = '01234567890abcdefghijklmnopqrstuvwxyz'

        # test that it matches when it should
        self.assertTrue(r.match(all_inclusive))
        self.assertTrue(r.match('t1_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t2_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t3_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t4_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t5_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t6_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t7_%s' % (all_inclusive,)))
        self.assertTrue(r.match('t8_%s' % (all_inclusive,)))

        # test that it doesn't match when it shouldn't
        self.assertFalse(r.match('t9_%s' % (all_inclusive,)))
        self.assertFalse(r.match('$!-.abc123'))
        self.assertFalse(r.match('$!-.'))

        # test that the group returns the item without the prefix
        self.assertEqual(r.match('t1_abc123').group(1), 'abc123')
        self.assertEqual(r.match('abc123').group(1), 'abc123')


    def test_post_id_regex(self):
        """
        Test that the post id regular expression behaves as expected.
        """
        r = SubredditSpider.post_id_regex

        all_inclusive = '01234567890abcdefghijklmnopqrstuvwxyz'

        # test that it matches
        self.assertTrue(r.match('t3_%s' % (all_inclusive,)))
        self.assertTrue(r.match(all_inclusive))

        # test that group 1 always gives us the id without the prefix
        self.assertEqual(r.match('t3_%s' % (all_inclusive,)).group(1), all_inclusive)
        self.assertEqual(r.match(all_inclusive).group(1), all_inclusive)

        # assert that we don't match other types
        self.assertFalse(r.match('t1_%s' % (all_inclusive,)))
        self.assertFalse(r.match('t9_%s' % (all_inclusive,)))



    def test_comment_id_regex(self):
        """
        Test that the comment id regular expression behaves as expected.
        """
        r = SubredditSpider.comment_id_regex

        all_inclusive = '01234567890abcdefghijklmnopqrstuvwxyz'

        # test that it matches
        self.assertTrue(r.match('t1_%s' % (all_inclusive,)))
        self.assertTrue(r.match(all_inclusive))

        # test that group 1 always gives us the id without the prefix
        self.assertEqual(r.match('t1_%s' % (all_inclusive,)).group(1), all_inclusive)
        self.assertEqual(r.match(all_inclusive).group(1), all_inclusive)

        # assert that we don't match other types
        self.assertFalse(r.match('t3_%s' % (all_inclusive,)))
        self.assertFalse(r.match('t9_%s' % (all_inclusive,)))


    def test_get_raw_id(self):
        """
        Test that get_raw_id returns a properly-formatted raw base36 id.
        """
        ref = SubredditSpider(None)

        # test totalli invalid id
        try:
            ref.get_raw_id('!-$.')
            self.fail("Failed to raise an exception on input of an improperly formatted id.")
        except InvalidIdException:
            pass

        # test value of invalid type
        try:
            ref.get_raw_id('t9_abc123')
            self.fail("Failed to raise an exception on input of in invalid type.")
        except InvalidIdException:
            pass

        self.assertEqual(ref.get_raw_id('t8_abc123'), 'abc123')
        self.assertEqual(ref.get_raw_id('t3_abc123'), 'abc123')
        self.assertEqual(ref.get_raw_id('abc123'), 'abc123')


    def test_get_post_id(self):
        """
        Test that get_post_id returns a properly-formatted post id.
        """
        ref = SubredditSpider(None)

        # test totally invalid id
        try:
            ref.get_post_id('!-$.')
            self.fail("Failed to raise an exception on input of an improperly formatted id.")
        except InvalidIdException:
            pass

        # test value of wrong type
        try:
            ref.get_post_id('t1_abc123')
            self.fail("Failed to raise an exception on input of an id of the wrong type.")
        except InvalidIdException:
            pass

        # test parsing
        self.assertEqual(ref.get_post_id('t3_abc123'), 't3_abc123')
        self.assertEqual(ref.get_post_id('abc123'), 't3_abc123')


    def test_get_comment_id(self):
        """
        Test that get_comment_id returns a properly-formatted comment id.
        """
        ref = SubredditSpider(None)

        # test totally invalid id
        try:
            ref.get_comment_id('!-$.')
            self.fail("Failed to raise an exception on input of an improperly formatted id.")
        except InvalidIdException:
            pass

        # test value of wrong type
        try:
            ref.get_comment_id('t3_abc123')
            self.fail("Failed to raise an exception on input of an id of the wrong type.")
        except InvalidIdException:
            pass

        # test parsing
        self.assertEqual(ref.get_comment_id('t1_abc123'), 't1_abc123')
        self.assertEqual(ref.get_comment_id('abc123'), 't1_abc123')
