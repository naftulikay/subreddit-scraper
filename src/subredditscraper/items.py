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

    # ids

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()

    """The full id of the comment with the `t1_` prefix."""
    comment_id = scrapy.Field()

    # post and parent relationships

    """The full id of the post/link that this comment is ultimately associated with."""
    post_id = scrapy.Field()

    """
    The full id of the parent of this comment.

    This can be either a post or a comment. If it is a post id (beginning with t3_), it is
    a top-level comment. If it is a comment id (beginning with t1_), it is a comment on a
    comment.
    """
    parent_id = scrapy.Field()

    # subreddit info

    """The name of the subreddit which this comment's post is in."""
    subreddit = scrapy.Field()

    """The full id of the subreddit (beginning with t5_)."""
    subreddit_id = scrapy.Field()

    # author info

    """The username of the author of this comment."""
    author = scrapy.Field()

    # body text

    """The Markdown text of the comment body."""
    body = scrapy.Field()

    """The rendered HTML text of the comment body."""
    body_html = scrapy.Field()

    # dates

    """The UTC time of creation of this comment."""
    created = scrapy.Field()

    """
    The UTC time of last modification of this comment.

    This value will be a boolean false if the comment was not edited.
    """
    edited = scrapy.Field()

    # scores

    


class SQLiteItemPipeline(object):
    pass
