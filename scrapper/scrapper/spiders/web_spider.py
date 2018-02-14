# -*- coding: utf-8 -*-
import scrapy


class WebSpider(scrapy.Spider):
    name = 'web'
    start_urls = ['https://doc.scrapy.org/en/latest/intro/overview.html']

    def parse(self, response):
        xpath = '//body//text()[normalize-space() and not(parent::script | parent::style | parent::a)]'
        text_nodes = response.xpath(xpath).extract()

        formatted_text = (' '.join(text_nodes))
        phrases = formatted_text.split('. ')

        for p in phrases:
            yield {
                'text': p
            }
