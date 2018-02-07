# -*- coding: utf-8 -*-
import scrapy

from scrapper.items import BrandItem
import os

from scrapper.helpers import send_result_to_bq

# Import the Google Cloud Storage Library
from google.cloud import storage


class BrandsSpiderSpider(scrapy.Spider):
    name = 'brands_spider'

    bucket_name = 'urlbucket'
    file_name = 'quotes_urls.txt'
    result_file_name = 'result.jl'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-file.json"

    def __init__(self):
        
        try:
            os.remove(self.result_file_name)
        except OSError:
            pass

        # Instantiates a client
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(self.bucket_name)
        blob = bucket.get_blob(self.file_name)
        file = blob.download_as_string()

        urls = file.splitlines()
        self.start_urls = urls

        for index, url in enumerate(self.start_urls):
            url = url.decode('utf-8')
            if url.endswith('/'):
                url = url[:-1]
                self.start_urls[index] = url

        print (self.start_urls)

    def parse(self, response):
        for sel in response.css('div.quote'):
            item = BrandItem()
            item['quote'] = sel.css('span.text::text').extract()
            item['author'] = sel.css('small.author::text').extract()
            item['tags'] = sel.css('.tag::text').extract()

            yield item

    def closed(self, reason):
        send_result_to_bq(self.result_file_name)

