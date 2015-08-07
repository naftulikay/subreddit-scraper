#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import scrapy

from subredditscraper.spiders import SubredditSpider


bool_serializer = lambda a: bool(a) if a is not None else None


def edited_serializer(a):
    """
    Serializes a float or boolean to a float or None.
    """
    if a is False:
        return None
    elif isinstance(a, (int, float, long)) or a is True:
        return float(a)
    else:
        return None


def id_serializer(a):
    """
    Serializes an ID by stripping its prefix.
    """
    if isinstance(a, (str, unicode)) and SubredditSpider.id_regex.match(a):
        return SubredditSpider.id_regex.match(a).group(1)
    else:
        return None


def link_id_serializer(a):
    """
    Serializes a link id by prefixing it if necessary.
    """
    return a


def comment_id_serializer(a):
    """
    Serializes a comment id by prefixing it if necessary.
    """
    return a


class Created(object):
    """
    An object that keeps track of when it was created.
    """

    """
    The time of creation in local epoch-second format.

    Description:
    (int) The time of creation in local epoch-second format. ex: 1331042771.0
    """
    created = scrapy.Field(serializer=float)

    """
    The time of creation in UTC epoch-second format. Note that neither of these ever have a non-zero fraction.

    Description:
    (int) the time of creation in UTC epoch-second format. Note that neither of these ever have a non-zero fraction.
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
    ups = scrapy.Field(serializer=int)

    """
    The amount of downvotes for this given object.

    Description:
    (int) the number of downvotes. (includes own)
    """
    downs = scrapy.Field(serializer=int)

    """
    True if the current user "likes" this object, false if the user "dislikes" this object, null if the user hasn't
    "liked" or "disliked" this object.

    Description:
    (Boolean) true if thing is liked by the user, false if thing is disliked, null if the user has not voted or you are
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

    """
    The base-36 id of the link.
    """
    id = scrapy.Field(serializer=id_serializer)

    """
    The prefixed base-36 id of the link.
    """
    prefixed_id = scrapy.Field(serializer=link_id_serializer)

    """
    The account name of the poster, null if it's a promotional link.

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
    Presumably whether the user has clicked this link.

    Description:
    (bool) probably always returns false
    """
    clicked = scrapy.Field(serializer=bool_serializer)

    """
    The domain name of this link.

    Description:
    (str) the domain of this link. Self posts will be self.<subreddit> while other examples include en.wikipedio.org
          and s3.amazon.com
    """
    domain = scrapy.Field()

    """
    Whether the post is hidden or not.

    Description:
    (boolean) true if the post is hidden by the logged in user. false if not logged in or not hidden.
    """
    hidden = scrapy.Field(serializer=bool)

    """
    Whether this link is a selfpost.

    Description:
    (boolean) true if this link is a selfpost.
    """
    is_self = scrapy.Field(serializer=bool)

    """
    The CSS class of the link's flair.

    Description:
    (str) the CSS class of the link's flair.
    """
    link_flair_css_class = scrapy.Field()

    """
    The text of the link's flair.

    Description:
    (str) the text of the link's flair.
    """
    link_flair_text = scrapy.Field()

    """
    Information on media relevant to the url.

    Description:
    (dict) Used for streaming video. Technical embed-specific information is found here.
    """
    media = scrapy.Field(serializer=unicode)

    """
    More information on embedded media relevant to the url.

    Description:
    (dict) Used for streaming video. Technical embed-specific information is found here.
    """
    media_embed = scrapy.Field(serializer=unicode)

    """
    The number of comments on this link.

    Description:
    (int) the number of comments that belong to this link. includes removed comments.
    """
    num_comments = scrapy.Field(serializer=int)

    """
    Whether the post is NSFW.

    Description:
    (bool) true if this post is tagged as NSFW. False if otherwise.
    """
    over_18 = scrapy.Field(serializer=bool)

    """
    The relative (to reddit.com) permalink for this link.

    Description:
    (str) relative URL of the permanent link for this link.
    """
    permalink = scrapy.Field()

    """
    Whether this post has been saved by the user.

    Description:
    (bool) true if this post is saved by the logged in user
    """
    saved = scrapy.Field(serializer=bool)

    """
    The net-score for the link.

    Description:
    (int) the net-score of the link.
    """
    score = scrapy.Field(serializer=int)

    """
    The raw Markdown text of the body.

    Description:
    (str) The raw text. this is the unformatted text which includes the raw markup characters such as ** for bold.
          <, >, and& are escaped. Empty if not present.
    """
    selftext = scrapy.Field()

    """
    The HTML generated text of the body from the raw Markdown.

    Description:
    (str) The formatted escaped HTML text. this is the HTML formatted version of the marked up text. Items that are
          boldened by ** or *** will now have <em> or *** tags on them. Additionally, bullets and numbered lists will
          now be in HTML list format. NOTE: The HTML string will be escaped. You must unescape to get the raw HTML. Null
          if not present.
    """
    selftext_html = scrapy.Field()

    """
    Name of the subreddit which this link belongs to.

    Description:
    (str) subreddit of thing excluding the /r/ prefix.
    """
    subreddit = scrapy.Field()

    """
    The prefixed base-36 id of the subreddit to which this post belongs.

    Description:
    (str) the id of the subreddit in which the link is located.
    """
    subreddit_id = scrapy.Field()

    """
    A full URL to the thumbnail for this link.

    Description:
    (str) full URL to the thumbnail for this link; "self" if this is a self post; "default" if a thumbnail is not
          available.
    """
    thumbnail = scrapy.Field()

    """
    The title of the link.

    Description:
    (str) the title of the link. may contain newlines for some reason
    """
    title = scrapy.Field()

    """
    The link of this post.

    Description:
    (str) the link of this post. the permalink if this is a self-post
    """
    url = scrapy.Field()

    """
    The edited time of this link or false if unedited.

    Description:
    (int) indicates if link has been edited. Will be the edit timestamp if the link has been edited and return false
           otherwise.
    """
    edited = scrapy.Field(serializer=edited_serializer)

    """
    Whether this post has been distinguished by moderators/admins.

    Description:
    (str) to allow determining whether they have been distinguished by moderators/admins. null = not distinguished,
          moderator = the green [M], admin = the red [A], special = various other special distinguishes
    """
    distinguished = scrapy.Field()

    """
    Whether this post has been set to be a sticky in this subreddit.

    Description:
    (bool) true if this post is set as the sticky in its subreddit.
    """
    stickied = scrapy.Field()


class Comment(scrapy.Item):
    """
    A model representing a single Reddit comment.

    Exact mapping of original field names from JSON. Arrays and dicts are serialized to strings. Description of fields
    are taken from Reddit's official wiki: https://github.com/reddit/reddit/wiki/JSON
    """

    """
    The base-36 id of this comment.
    """
    id = scrapy.Field(serializer=id_serializer)

    """
    The prefixed base-36 id of this comment.
    """
    prefixed_id = scrapy.Field(serializer=comment_id_serializer)

    """
    The username of the approver of this comment.

    Description:
    (str) who approved this comment. null if nobody or you are not a mod
    """
    approved_by = scrapy.Field()

    """
    The account name of the poster.

    Description:
    (str) the account name of the poster.
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
    The username of the user which banned this comment.

    Description;
    (str) who removed this comment. null if nobody or you are not a mod
    """
    banned_by = scrapy.Field()

    """
    The raw Markdown text of the comment.

    Description:
    (str) the raw text. this is the unformatted text which includes the raw markup characters such as ** for bold. <,
          >, and & are escaped.
    """
    body = scrapy.Field()

    """
    The formatted HTML text of the comment generated from the raw Markdown text.

    Description:
    (str) the formatted HTML text as displayed on reddit. For example, text that is emphasised by * will now have <em>
          tags wrapping it. Additionally, bullets and numbered lists will now be in HTML list format. NOTE: The HTML
          string will be escaped. You must unescape to get the raw HTML.
    """
    body_html = scrapy.Field()

    """
    The last time this comment was edited, or false if it was never edited.

    Description:
    (int) false if not edited, edit date in UTC epoch-seconds otherwise. NOTE: for some old edited comments on
           reddit.com, this will be set to true instead of edit date.
    """
    edited = scrapy.Field(serializer=edited_serializer)

    """
    How many times this comment has been gilded

    Description:
    (int) the number of times this comment received reddit gold
    """
    gilded = scrapy.Field(serializer=int)

    """
    The link author's username.

    Description:
    (str) present if the comment is being displayed outside its thread (user pages, /r/subreddit/comments/.json, etc.).
          Contains the author of the parent link
    """
    link_author = scrapy.Field()

    """
    The id of the link this comment belongs to.

    Description:
    (str) ID of the link this comment is in
    """
    link_id = scrapy.Field(serializer=id_serializer)

    """
    The title of the link this comment belongs to.

    Description:
    (str) present if the comment is being displayed outside its thread (user pages, /r/subreddit/comments/.json, etc.).
          Contains the title of the parent link
    """
    link_title = scrapy.Field()

    """
    The URL of the link this comment belongs to.

    Description:
    (str) present if the comment is being displayed outside its thread (user pages, /r/subreddit/comments/.json, etc.).
          Contains the URL of the parent link
    """
    link_url = scrapy.Field()

    """
    The number of reports that this comment has accumulated.

    Description:
    (int) how many times this comment has been reported, null if not a mod
    """
    num_reports = scrapy.Field(serializer=int)

    """
    The parent ID of the thing this comment belongs to.

    Description:
    (str) ID of the thing this comment is a reply to, either the link or a comment in it
    """
    parent_id = scrapy.Field()

    """
    Whether this comment has been saved by the current user.

    Description:
    (bool) true if this post is saved by the logged in user
    """
    saved = scrapy.Field(serializer=bool)

    """
    The net-score of this comment.

    Description:
    (int) the net-score of the comment
    """
    score = scrapy.Field(serializer=int)

    """
    Whether this comment's score is hidden.

    Description:
    (bool) Whether the comment's score is currently hidden.
    """
    score_hidden = scrapy.Field(serializer=bool)

    """
    The name of the subreddit to which this comment and its link belong.

    Description:
    (str) subreddit of thing excluding the /r/ prefix. "pics"
    """
    subreddit = scrapy.Field()

    """
    The prefixed base-36 ID of the subreddit to which this comment and its link belong.

    Description:
    (str) the id of the subreddit in which the thing is located
    """
    subreddit_id = scrapy.Field()

    """
    The status of this comment's being distinguished.

    Description:
    (str) to allow determining whether they have been distinguished by moderators/admins. null = not distinguished.
    moderator = the green [M]. admin = the red [A]. special = various other special distinguishes
    """
    distinguished = scrapy.Field()


class SQLiteItemPipeline(object):
    pass
