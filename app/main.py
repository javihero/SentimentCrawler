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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'content': ''
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START scrapy_call]
class ScrapyCall(webapp2.RequestHandler):

    def post(self):
        url = self.request.get('url')
        api_url = 'http://localhost:9080/crawl.json?spider_name=rss&url=' + url

        content = urllib2.urlopen(api_url).read()
        json_content = json.loads(content)
        items = json_content['items']

        print items

        template_values = {
            'content': items
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END scrapy_call]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/scrap', ScrapyCall)
], debug=True)
# [END app]
