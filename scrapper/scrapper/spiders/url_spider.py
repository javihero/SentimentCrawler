# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class UrlSpider(CrawlSpider):
    name = 'url'

    # Last comma is SUPER important - Rule is not an iterable
    # Depth is in settings.py
    rules = (Rule(LinkExtractor(), callback='parse_url', follow=True),)

    def parse_url(self, response):
        xpath = '//body//text()[normalize-space() and not(parent::script | parent::style | parent::a)]'
        text_nodes = response.xpath(xpath).extract()

        formatted_text = (' '.join(text_nodes))
        phrases = formatted_text.split('. ')

        for p in phrases:
            if p is not '':
                yield {
                    'text': p
                }
