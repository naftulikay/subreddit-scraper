#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import scrapy


bool_serializer = lambda a: bool(a) if a is not None else None


class Created(object):
    """
    An object that keeps track of when it was created.
    """

    """
    The time of creation in local epoch-second format.

    Description:
    (long) The time of creation in local epoch-second format. ex: 1331042771.0
    """
    created = scrapy.Field(serializer=float)

    """
    The time of creation in UTC epoch-second format. Note that neither of these ever have a non-zero fraction.

    Description:
    (long) the time of creation in UTC epoch-second format. Note that neither of these ever have a non-zero fraction.
    """
    created_utc = scrapy.Field(serializer=float)


class Votable(object):
    """
    An object that can be voted upon, taken from Reddit's documentation.
    """

    """
    The amount of upvotes for this given object.

    Description:
    (int) the number of upvotes. (includes own)
    """
    ups = scrapy.Field(serializer=long)

    """
    The amount of downvotes for this given object.

    Description:
    (int) the number of downvotes. (includes own)
    """
    downs = scrapy.Field(serializer=long)

    """
    True if the current user "likes" this object, false if the user "dislikes" this object, null if the user hasn't
    "liked" or "disliked" this object.

    Description:
    (boolean) true if thing is liked by the user, false if thing is disliked, null if the user has not voted or you are
              not logged in. Certain languages such as Java may need to use a boolean wrapper that supports null
              assignment.
    """
    likes = scrapy.Field(serializer=bool_serializer)


class Link(scrapy.Item, Created, Votable):
    """
    A model representing a single Reddit link.

    Exact mapping of original field names from JSON. Arrays and dicts are serialized to strings. Descriptions of fields
    are taken from Reddit's official wiki: https://github.com/reddit/reddit/wiki/JSON
    """

    """An id encoded in base-36 without any prefixes."""
    id = scrapy.Field()

    """
    The username of the user that approved this comment. (String)

    Description:
    (str) who approved this comment. null if nobody or you are not a mod
    """
    approved_by = scrapy.Field()

    """
    Whether this post has been archived. No documentation found for this field in Reddit's docs.
    """
    archived = scrapy.Field()

    """
    The username of the creating user of this post.

    Description:
    (str) the account name of the poster. null if this is a promotional link
    """
    author = scrapy.Field()

    """
    The CSS class of the author's flair.

    Description:
    (str) the CSS class of the author's flair. subreddit specific
    """
    author_flair_css_class = scrapy.Field()

    """
    The text of the author's flair.

    Description:
    (str) the text of the author's flair. subreddit specific
    """
    author_flair_text = scrapy.Field()

    """

    Description:
    (str)
    """
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
    A model representing a single Reddit comment.

    Exact mapping of original field names from JSON. Arrays and dicts are serialized to strings. Description of fields
    are taken from Reddit's official wiki: https://github.com/reddit/reddit/wiki/JSON
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
