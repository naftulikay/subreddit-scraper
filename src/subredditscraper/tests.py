#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest

from subredditscraper.exceptions import InvalidIdException

from subredditscraper.items import (
    bool_serializer,
    edited_serializer,
)

from subredditscraper.spiders import SubredditSpider


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
        self.assertEqual(1.0, edited_serializer(True))
        # test string value
        self.assertEqual(None, edited_serializer('nope'))
        # convert long to float
        self.assertEqual(3.0, edited_serializer(3L))
        # convert float to float
        self.assertEqual(3.0, edited_serializer(3.0))
        # convert int to float
        self.assertEqual(3.0, edited_serializer(3))


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
