#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import scrapy


class Post(scrapy.Item):
    """
    A model representing a single Reddit post.

    Exact mapping of original field names from JSON. Arrays and dicts are serialized to strings.
    """

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()

    approved_by = scrapy.Field()
    archived = scrapy.Field()
    author = scrapy.Field()
    author_flair_css_class = scrapy.Field()
    banned_by = scrapy.Field()
    clicked = scrapy.Field()
    domain = scrapy.Field()
    downs = scrapy.Field()
    edited = scrapy.Field()
    from_kind = scrapy.Field()
    gilded = scrapy.Field()
    hidden = scrapy.Field()
    hide_score = scrapy.Field()
    likes = scrapy.Field()
    link_flair_css_class = scrapy.Field()
    link_flair_text = scrapy.Field()
    media = scrapy.Field()
    media_embed = scrapy.Field()
    num_comments = scrapy.Field()
    over_18 = scrapy.Field()
    report_reasons = scrapy.Field()
    score = scrapy.Field()
    secure_media = scrapy.Field()
    secure_media_embed = scrapy.Field()
    selftext = scrapy.Field()
    selftext_html = scrapy.Field()
    subreddit = scrapy.Field()
    subreddit_id = scrapy.Field()
    suggested_sort = scrapy.Field()
    thumbnail = scrapy.Field()
    user_reports = scrapy.Field()


class Comment(scrapy.Item):
    """
    A model representing a single Reddit comment
    """

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()

    approved_by = scrapy.Field()
    archived = scrapy.Field()
    author = scrapy.Field()
    author_flair_css_class = scrapy.Field()
    author_flair_text = scrapy.Field()
    banned_by = scrapy.Field()
    body = scrapy.Field()
    body_html = scrapy.Field()
    controversiality = scrapy.Field()
    created = scrapy.Field()
    created_utc = scrapy.Field()
    distinguished = scrapy.Field()
    downs = scrapy.Field()
    edited = scrapy.Field()
    gilded = scrapy.Field()
    likes = scrapy.Field()
    link_id = scrapy.Field()
    mod_reports = scrapy.Field()
    name = scrapy.Field()
    num_reports = scrapy.Field()
    parent_id = scrapy.Field()
    removal_reason = scrapy.Field()
    replies = scrapy.Field()
    report_reasons = scrapy.Field()
    saved = scrapy.Field()
    score = scrapy.Field()
    score_hidden = scrapy.Field()
    subreddit = scrapy.Field()
    subreddit_id = scrapy.Field()
    ups = scrapy.Field()
    user_reports = scrapy.Field()


class SQLiteItemPipeline(object):
    pass
