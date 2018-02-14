#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Twitter API calls are made from here
"""

from twitter_config import API_KEY, API_SECRET, OAUTH_KEY, OAUTH_SECRET
import twitter


class TwitterService():
    api = twitter.Api(consumer_key=API_KEY,
                      consumer_secret=API_SECRET,
                      access_token_key=OAUTH_KEY,
                      access_token_secret=OAUTH_SECRET)

    def verify_credentials(self):
        return self.api.VerifyCredentials()

    def get_tweets_from(self, term):
        info = []

        # result = self.api.GetSearch(
        # raw_query="q=from%3A" + term)

        result = self.api.GetUserTimeline(
            screen_name=term, count=100, exclude_replies=True)

        for status in result:
            info.append(status)

        return info
