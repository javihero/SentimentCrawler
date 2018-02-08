# -*- coding: utf-8 -*-
import scrapy


class QuotesUrlSpider(scrapy.Spider):
    name = 'quoteurls'
    start_urls = []

    def parse(self, response):
        for sel in response.css('div.quote'):
            yield {
                'quote': sel.css('span.text::text').extract(),
                'author': sel.css('small.author::text').extract(),
                'tags': sel.css('.tag::text').extract()
            }
