#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Twitter API calls are made from here
"""

from twitter_config import API_KEY, API_SECRET, OAUTH_KEY, OAUTH_SECRET
import requests
from requests_oauthlib import OAuth1


class TwitterService():
    base_url = 'https://api.twitter.com/1.1/'
    auth_url = base_url + 'account/verify_credentials.json'
    auth = OAuth1(API_KEY, API_SECRET,
                  OAUTH_KEY, OAUTH_SECRET)

    def get_tweets(self):
        r = requests.get(
            self.base_url + 'statuses/user_timeline.json?screen_name=stackoverflow&count=100', auth=self.auth)

        for tweet in r.json():
            print tweet['text']
