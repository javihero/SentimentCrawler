# -*- coding: utf-8 -*-
import scrapy
from scrapper.helpers import sanitize_content


class WebSpider(scrapy.Spider):
    name = 'web'

    def parse(self, response):
        xpath = '//body//text()[normalize-space() and not(parent::script | parent::style | parent::a)]'
        text_nodes = response.xpath(xpath).extract()

        formatted_text = (' '.join(text_nodes))
        phrases = formatted_text.split('. ')

        for p in phrases:
            if p is not '':
                yield {
                    'text': sanitize_content(p)
                }
