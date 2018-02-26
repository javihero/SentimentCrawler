# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class UrlSpider(CrawlSpider):
    name = 'url'

    # Last comma is SUPER important - Rule is not an iterable
    # Depth is in settings.py
    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True),)

    def parse_url(self, response):
        yield {'url': response.url}
