#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib2
import json

import jinja2
import webapp2

import csv

# Import the Google Cloud Storage Library
import cloudstorage as gcs

from twitter_service import TwitterService

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
# [END retries]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'content': ''
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START scrapy_rss]
class ScrapyRss(webapp2.RequestHandler):

    def post(self):
        url = self.request.get('url')
        spider = 'rss'
        api_url = 'http://localhost:9080/crawl.json?spider_name=' + spider + '&url=' + url

        content = urllib2.urlopen(api_url).read()
        json_content = json.loads(content)
        items = json_content['items']

        template_values = {
            'content': items
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END scrapy_rss]


# [START scrapy_atom]
class ScrapyAtom(webapp2.RequestHandler):

    def post(self):
        url = self.request.get('url')
        spider = 'atom'
        api_url = 'http://localhost:9080/crawl.json?spider_name=' + spider + '&url=' + url

        content = urllib2.urlopen(api_url).read()
        json_content = json.loads(content)
        items = json_content['items']

        template_values = {
            'content': items
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END scrapy_atom]


# [START scrapy_web]
class ScrapyWeb(webapp2.RequestHandler):

    def post(self):
        url = self.request.get('url')
        spider = 'web'
        api_url = 'http://localhost:9080/crawl.json?spider_name=' + spider + '&url=' + url

        content = urllib2.urlopen(api_url).read()
        json_content = json.loads(content)
        info = json_content['items']

        template_values = {
            'info': info
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END scrapy_web]


# [START twitter]
class RequestTwitter(webapp2.RequestHandler):

    def post(self):
        term = self.request.get('term')

        twitter = TwitterService()
        info = twitter.get_tweets_from(term)

        template_values = {
            'info': info
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END twitter]


# [START read brands, media and kind]
class CloudStorage(webapp2.RequestHandler):

    buck_name = 'urlbucket'
    brands_file_name = 'brands.csv'
    media_file_name = 'medios.csv'

    def get(self):

        bucket_name = os.environ.get('BUCKET_NAME', self.buck_name)

        kinds = ['website', 'rss', 'twitter']

        bucket = '/' + bucket_name
        brands_filename = bucket + '/' + self.brands_file_name
        media_filename = bucket + '/' + self.media_file_name
        self.tmp_filenames_to_clean_up = []

        try:
            brands = self.read_file(brands_filename)
            medios = self.read_file(media_filename)
        except Exception, e:
            self.response.write(e)

        template_values = {
            'brands': brands,
            'medios': medios,
            'tipos': kinds
        }

        template = JINJA_ENVIRONMENT.get_template('buckets.html')
        self.response.write(template.render(template_values))

    def post(self):

        bucket_name = os.environ.get('BUCKET_NAME', self.buck_name)

        kinds = ['website', 'rss', 'twitter']

        bucket = '/' + bucket_name
        brands_filename = bucket + '/' + self.brands_file_name
        media_filename = bucket + '/' + self.media_file_name
        self.tmp_filenames_to_clean_up = []

        try:
            brands = self.read_file(brands_filename)
            medios = self.read_file(media_filename)
        except Exception, e:
            self.response.write(e)

        brand_selected = self.request.get('brand')
        medio_selected = self.request.get('medio')
        kind_selected = self.request.get('kind')

        # ----- Take URLs ----- #

        url_file_name = ''

        if (kind_selected == 'website'):
            url_file_name = 'website.csv'
        elif (kind_selected == 'rss'):
            url_file_name = 'rss.csv'
        else:
            url_file_name = 'twitter.csv'

        url_filename = bucket + '/' + url_file_name

        try:
            urls = self.read_urls_file(url_filename, medio_selected)
        except Exception, e:
            self.response.write(e)

        template_values = {
            'brands': brands,
            'medios': medios,
            'tipos': kinds,
            'brand_selected': brand_selected,
            'medio_selected': medio_selected,
            'kind_selected': kind_selected,
            'urls': urls
        }

        template = JINJA_ENVIRONMENT.get_template('buckets.html')
        self.response.write(template.render(template_values))

    def read_file(self, filename):
        gcs_file = gcs.open(filename)
        readCSV = csv.reader(gcs_file, delimiter=',')
        for row in readCSV:
            yield str(row[0]).decode('utf-8')
        gcs_file.close()

    def read_urls_file(self, filename, medio_selected):
        gcs_file = gcs.open(filename)
        readCSV = csv.reader(gcs_file, delimiter=',')
        for row in readCSV:
            if (medio_selected == str(row[1]).decode('utf-8')):
                yield str(row[0]).decode('utf-8')
        gcs_file.close()

# [END brands]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/rss', ScrapyRss),
    ('/atom', ScrapyAtom),
    ('/web', ScrapyWeb),
    ('/twitter', RequestTwitter),
    ('/gcs', CloudStorage)
], debug=True)
# [END app]
