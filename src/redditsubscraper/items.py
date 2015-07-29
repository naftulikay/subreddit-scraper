#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import scrapy


class Post(scrapy.Item):
    """
    A model representing a single Reddit post.
    """
    id = scrapy.Field()


class Comment(scrapy.Item):
    """
    A model representing a single Reddit comment
    """
    id = scrapy.Field()
    parent_id = scrapy.Field()


class RedditItemPipeline(object):
    pass
