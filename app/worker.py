import webapp2

# Import the Google Cloud BigQuery Library
# from google.cloud import bigquery

# from io import StringIO

from helpers import request_scrapy
from google.appengine.api import taskqueue

"""
class BigQueryHandler(webapp2.RequestHandler):
    def post(self):
        item = self.request.get('item')

        def send_scrapper_result_to_bigquery(item):

            dataset_name = 'sentimentcrawlerdataset'
            table_id = 'scrapper_table'

            bigquery_client = bigquery.Client()
            dataset_ref = bigquery_client.dataset(dataset_name)
            table_ref = dataset_ref.table(table_id)

            job_config = bigquery.LoadJobConfig()
            job_config.source_format = 'NEWLINE_DELIMITED_JSON'
            job_config.autodetect = True

            # load_job = bigquery_client.load_table_from_uri('https://storage.cloud.google.com' + source_file_name, table_ref, job_config=job_config)  # API request
            load_job = bigquery_client.load_table_from_file(
                StringIO(unicode(item)), table_ref, job_config=job_config)  # API request

            load_job.result()  # Waits for table load to complete.

        send_scrapper_result_to_bigquery(item)
"""


# [START crawler tasks]
class ScrapyHandler(webapp2.RequestHandler):
    def post(self):
        url = self.request.get('url')
        depth = 0

        # Requests text and list of urls from url, will stop when depth is 3
        taskqueue.add(url='/request_urls',
                      params={'url': url, 'depth': depth})


class ScrapyUrlHandler(webapp2.RequestHandler):
    """
    Recursive function, take care
    """

    def post(self):
        url = self.request.get('url')
        depth = int(self.request.get('depth'))
        api_url = 'http://localhost:9080/crawl.json?spider_name=url&url=' + url

        # Fire a task to request text from the caller url
        taskqueue.add(url='/request_text',
                      params={'url': url})

        if depth < 3:

            depth += 1

            # Returns list of urls found
            urls = request_scrapy(api_url)

            for row in urls:
                url = row['url']

                # Fire this same task to request text + urls from each url in list
                taskqueue.add(url='/request_urls',
                              params={'url': url, 'depth': depth})


class ScrapyTextHandler(webapp2.RequestHandler):
    """
    URL --> Text
    """

    def post(self):
        url = self.request.get('url')
        api_url = 'http://localhost:9080/crawl.json?spider_name=web&url=' + url

        # Returns list of text found
        text = request_scrapy(api_url)

        # Dict { url: '', lines: [] }
        result = {}
        result['url'] = url
        result['lines'] = []
        for line in text:
            result['lines'].append(line)

        # WIP add task to send result to BigQuery
# [END crawler tasks]


app = webapp2.WSGIApplication([
    # ('/send_bq', BigQueryHandler),
    ('/request_urls', ScrapyUrlHandler),
    ('/request_text', ScrapyTextHandler),
    ('/request_crawler', ScrapyHandler)
], debug=True)
# [END all]
