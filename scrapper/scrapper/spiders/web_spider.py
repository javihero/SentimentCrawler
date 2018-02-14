# -*- coding: utf-8 -*-
import scrapy


class WebSpider(scrapy.Spider):
    name = 'web'
    start_urls = ['https://doc.scrapy.org/en/latest/intro/overview.html']

    def parse(self, response):
        result_list = []
        text_nodes = response.xpath('//text()').extract()

        text_list = ('\n'.join(text_nodes)).splitlines()
        text_list = filter(lambda a: a != '', text_list)

        for line in text_list:
            if not line.isspace():
                result_list.append(line.strip())

        formatted_text = (' '.join(result_list))
        phrases = formatted_text.split('. ')

        for p in phrases:
            yield {
                'text': p
            }
