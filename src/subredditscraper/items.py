#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import scrapy


class Post(scrapy.Item):
    """
    A model representing a single Reddit post.
    """

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()


class Comment(scrapy.Item):
    """
    A model representing a single Reddit comment
    """

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()

    parent_id = scrapy.Field()


class RedditItemPipeline(object):
    pass
