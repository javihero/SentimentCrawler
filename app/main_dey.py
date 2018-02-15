#!/usr/bin/env python
# -*- coding: utf-8 -*-

# [START imports]
import logging
import os
import urllib

from google.appengine.api import users

import jinja2
import webapp2

import csv

# Import the Google Cloud Storage Library
import cloudstorage as gcs
from google.appengine.api import app_identity



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

#[START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                        max_delay=5.0,
                                        backoff_factor=2,
                                        max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]


# [START main_page]
class MainPage(webapp2.RequestHandler):
    
    def get(self):
        
        template_values = {
            'content': ''
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

# [END main_page]


# [START read brands, media and kind]
class readBrandsMedia(webapp2.RequestHandler):
    
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
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
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

        ######## Take URLs #########

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
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
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




# [START READ URL/ACCOUNT FOR SCRAPPER]
"""
class readForScapper(webapp2.RequestHandler):
    
    buck_name = 'urlbucket'
    file_name = 'libbys_rss.csv'

    def get(self):
        
        bucket_name = os.environ.get('BUCKET_NAME', self.buck_name)
        self.response.headers['Content-Type'] = 'text/plain;charset=UTF-8'
        self.response.write('Demo GCS Application running from Version: ' + os.environ['CURRENT_VERSION_ID'] + '\n')
        self.response.write('Using bucket name: ' + bucket_name + '\n\n')

        bucket = '/' + bucket_name
        filename = bucket + '/' + self.file_name
        self.tmp_filenames_to_clean_up = []

        try:
            
            self.read_file(filename)
            self.response.write('\n\n')

        except Exception, e:
            self.response.write('\n\nThere was an error running the demo! '
                          'Please check the logs for more details.\n')

    # [START read]
    def read_file(self, filename):
        self.response.write('Reading the full file contents:\n')
        gcs_file = gcs.open(filename)
        readCSV = csv.reader(gcs_file, delimiter=',')
        for row in readCSV:
            self.response.write('URL RSS: ' + row[0] + '\n')         
        gcs_file.close()

        #self.response.write(contents)
    # [END read]
    
# [END READ BUCKET]
"""

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/readbrands', readBrandsMedia)
], debug=True)
# [END app]
