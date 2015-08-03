#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import logging
import re
import scrapy

from subredditscraper.exceptions import InvalidIdException
from urllib import urlencode

logger = logging.getLogger('subredditscraper.spiders')


class SubredditSpider(scrapy.spiders.Spider):
    """

    Notes to self:

    Types:
      * t1_ - comment
      * t2_ - account
      * t3_ - link
      * t4_ - message
      * t5_ - subreddit
      * t6_ - award
      * t8_ - promo campaign

    Single comment GET:
        https://www.reddit.com/r/woahdude/comments/3f6fp6/new.json?depth=1&comment=ctly7f4&sort=new&showmore=false
        https://www.reddit.com/r/woahdude/comments/3f6fp6/new.json?depth=1&comment=cto4lbd&sort=new&showmore=false

    We want a depth of 1 (ie _only_ the comment itself), not to show more, sort by new, and for the above request,
    we select the specific comment we want. By removing the comment parameter, we'll get a listing of comments for
    the article without any depth, which is what we want.

    Multi post/link GET:
        https://www.reddit.com/r/woahdude/new.json?sort=new&limit=5

    Multi post/link GET more (before last post of previous request):
        https://www.reddit.com/r/woahdude/new.json?sort=new&limit=5&before=3fn7gg

    Multi comment GET:
        https://www.reddit.com/r/woahdude/comments/3f6fp6/new.json?depth=1&sort=new&showmore=false

    Multi comment GET more (before last post of previous request):
        https://www.reddit.com/r/woahdude/comments/3f6fp6/new.json?depth=1&sort=new&showmore=false&before=ctmlaqo&limit=5

    Here's the process for scraping Reddit.

    1. GET https://www.reddit.com/r/$sub_name/new.json?sort=new
    2. For each post in 'data.children':
        2a. GET https://www.reddit.com/r/$sub_name/comments/$post_id/new.json?sort=new
        2b. While length of 'data.children' is greater than zero:
          2b1. last_comment = data.children[data.children.length - 1].id
          2b2. GET https://www.reddit.com/r/$sub_name/comments/$post_id/new.json?sort=new&before=t1_$last_comment
    3. While length of 'data.children' is greater than zero:
        3a. last_post = data.children[data.children.length - 1].id
        3b. GET https://www.reddit.com/r/$sub_name/new.json?sort=new?before=t3_$last_post
        3c. Return to step 2 to process the children

    """

    id_regex = re.compile(r'\b(?:t[1-8]_)?([0-9a-z]+)\b')

    post_id_regex = re.compile(r'\b(?:t3_)?([0-9a-z]+)\b')

    comment_id_regex = re.compile(r'\b(?:t1_)?([0-9a-z]+)\b')

    def __init__(self, subreddit_name):
        self.subreddit_name = subreddit_name

    def start_requests(self):
        return [
            self.request('https://www.reddit.com/r/%(subreddit_name)/new.json' % {'subreddit_name': self.subreddit_name},
                params={'sort': 'new'})
        ]

    def get_posts(self, before=None):
        """
        Get the newest posts of this sub, optionally posts before a given post.

        Arguments:
        before: A base36 ID of a Reddit 'link' (in their terminology, what we refer to as a post).
                This value can match either `[0-9a-z]+` or `t3_[0-9a-z]+`.
        """
        params = {
            'sort': 'new',
        }

        if not self.post_id_regex.match(before):
            raise Exception('Invalid post id %s' % (before,))
        else:
            # format as t3_%(id)s
            params['before'] = 't3_%(id)s' % {'id': self.post_id_regex.match(before).group(1)}

        return self.request(
            'https://www.reddit.com/r/%(subreddit_name)/new.json' % {'subreddit_name': self.subreddit_name},
            params=params
        )


    def get_comments(self, post_id, before=None):
        """
        Get the newest comments for a given post, optionally before a given comment.

        Arguments:
        post_id: The base36 id for the Reddit post.
        before: A base36 id of a Reddit comment. If specified, the comments returned by this request
                will have been posted chronologically _before_ the comment specified.
        """
        pass


    def request(self, url, params=None, **kwargs):
        """
        Fancy method for making a scrapy.Request object using a URL and query parameters
        in the form of a dictionary.

        Arguments:
        url: The URL to make a GET request for.
        params: A dictionary of query parameters to append to the URL string.
        **kwargs: Keyword arguments passed to the constructor of the request.

        Returns:
        A scrapy.Request object with the given ultimate URL.
        """
        if params:
            # set the URL to
            url = '?'.join(url, urlencode(params)) if not url.endswith('?') else ''.join(url, urlencode(params))

        return scrapy.Request(url, **kwargs)


    def get_raw_id(self, id):
        """
        Gets the raw base36 id of any Reddit object type, stripping the prefix.

        Returns:
        The base36 id of a given item in Reddit without the prefix.
        """
        if not self.id_regex.match(id):
            raise InvalidIdException('%s is not a valid Reddit base36 id.' % (id,))

        return self.id_regex.match(id).group(1)


    def get_post_id(self, id):
        """
        Gets the prefixed base36 id of a Reddit post object, based on an input id.

        Returns:
        A prefixed base36 id for a Reddit post object. (`t3_[0-9a-z]+`)
        """
        if not self.post_id_regex.match(id):
            raise InvalidIdException('%s is not a valid Reddit post id.' % (id,))

        return 't3_%s' % (self.post_id_regex.match(id).group(1),)


    def get_comment_id(self, id):
        """
        Gets the prefixed base36 id of a Reddit comment object, based on an input id.

        Returns:
        A prefixed base36 id for a Reddit comment object. (`t1_[0-9a-z]+`)
        """
        if not self.comment_id_regex.match(id):
            raise InvalidIdException('%s is not a valid Reddit comment id.' % (id,))

        return 't1_%s' % (self.comment_id_regex.match(id).group(1))
