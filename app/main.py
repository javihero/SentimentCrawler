#!/usr/bin/env python
# -*- coding: utf-8 -*-

# [START imports]
import os

import jinja2
import webapp2

import csv
import json

# Import the Google Cloud Storage Library
import cloudstorage as gcs
from google.appengine.api import urlfetch

from natural_service import NaturalService
from twitter_service import TwitterService
from helpers import sanitize_url, request_scrapy
from google.appengine.api import taskqueue
# from bigquery_service import send_scrapper_result_to_bigquery

import logging
logging.basicConfig(level=logging.DEBUG)


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


# [START Scrapy URL]
local_url = 'http://localhost:9080'
cloud_url = 'http://35.197.243.127'

current_url = local_url
# [END Scrapy URL]


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
        url = sanitize_url(url)
        spider = 'rss'
        api_url = current_url + '/crawl.json?spider_name=' + spider + '&url=' + url

        items = request_scrapy(api_url)

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
        url = sanitize_url(url)
        spider = 'atom'
        api_url = current_url + '/crawl.json?spider_name=' + spider + '&url=' + url

        items = request_scrapy(api_url)

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
        url = sanitize_url(url)

        # Request text and urls from the 1st url
        taskqueue.add(url='/request_crawler', target='worker',
                      params={'url': url})

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

# [END scrapy_web]


# [START twitter]
class RequestTwitter(webapp2.RequestHandler):

    def post(self):
        term = self.request.get('term')
        twitter = TwitterService()
        info = twitter.search_tweets(term)

        template_values = {
            'content': info
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END twitter]


# [START natural_language]
class RequestNaturalLanguage(webapp2.RequestHandler):

    def get(self):
        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('natural.html')
        self.response.write(template.render(template_values))

    def post(self):
        text = self.request.get('text')

        natural = NaturalService()
        response = natural.request_sentiment(text)

        template_values = {
            'content': response
        }

        template = JINJA_ENVIRONMENT.get_template('natural.html')
        self.response.write(template.render(template_values))
# [END natural_language]


# [START read brands, media and kind]
class CloudStorage(webapp2.RequestHandler):

    buck_name = 'urlbucket'
    brands_file_name = 'brands.csv'
    media_file_name = 'medios.csv'
    bucket_name = os.environ.get('BUCKET_NAME', buck_name)
    kinds = ['website', 'rss', 'twitter']

    bucket = '/' + bucket_name
    brands_filename = bucket + '/' + brands_file_name
    media_filename = bucket + '/' + media_file_name
    tmp_filenames_to_clean_up = []

    def get(self):

        try:
            brands = self.read_file(self.brands_filename)
            medios = self.read_file(self.media_filename)
        except Exception, e:
            self.response.write(e)

        template_values = {
            'brands': brands,
            'medios': medios,
            'tipos': self.kinds
        }

        template = JINJA_ENVIRONMENT.get_template('buckets.html')
        self.response.write(template.render(template_values))

    def post(self):

        try:
            brands = self.read_file(self.brands_filename)
            medios = self.read_file(self.media_filename)
        except Exception, e:
            self.response.write(e)

        # brand_selected = self.request.get('brand')
        medio_selected = self.request.get('medio')
        kind_selected = self.request.get('kind')

        # ----- Take URLs ----- #

        url_file_name = ''

        if (kind_selected == 'website'):
            url_file_name = 'website.csv'
            spider = 'web'
        elif (kind_selected == 'rss'):
            url_file_name = 'rss.csv'
            spider = 'rss'
        else:
            url_file_name = 'twitter.csv'

        url_filename = self.bucket + '/' + url_file_name

        try:
            urls = self.read_urls_file(url_filename, medio_selected)
        except Exception, e:
            self.response.write(e)

        # Request loop

        result = []
        for url in urls:
            info = {}
            info['url'] = url

            if kind_selected == 'twitter':
                twitter = TwitterService()
                response = twitter.get_tweets_from(url)
            else:
                api_url = current_url + '/crawl.json?spider_name=' + spider + '&url=' + url
                response = request_scrapy(api_url)

            info['text'] = response

            result.append(info)

        # Render result

        template_values = {
            'brands': brands,
            'medios': medios,
            'tipos': self.kinds,
            'result': result
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
    ('/gcs', CloudStorage),
    ('/natural', RequestNaturalLanguage)
], debug=True)
# [END app]
