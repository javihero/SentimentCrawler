#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitter_config import API_KEY, API_SECRET, OAUTH_KEY, OAUTH_SECRET
import twitter


class TwitterService():
    """
    Twitter API calls are made from here
    """

    api = twitter.Api(consumer_key=API_KEY,
                      consumer_secret=API_SECRET,
                      access_token_key=OAUTH_KEY,
                      access_token_secret=OAUTH_SECRET)

    def verify_credentials(self):
        return self.api.VerifyCredentials()

    def get_tweets_from(self, term):
        return self.api.GetUserTimeline(
            screen_name=term, count=100, exclude_replies=True)
