import webapp2

# Import the Google Cloud BigQuery Library
from google.cloud import bigquery
from google.cloud.bigquery import Dataset

import os
import logging

import ssl
from io import StringIO


class BigQueryHandler(webapp2.RequestHandler):
    def post(self):
        item = self.request.get('item')
        bq_client = self.request.get('bq_client')
        table_ref = self.request.get('table_ref')
        job_config = self.request.get('job_config')

        def send_scrapper_result_to_bigquery(bq_client, table_ref, job_config, item):

            #load_job = bigquery_client.load_table_from_uri('https://storage.cloud.google.com' + source_file_name, table_ref, job_config=job_config)  # API request
            load_job = bq_client.load_table_from_file(StringIO(unicode(item)), table_ref, job_config=job_config) # API request

            load_job.result()  # Waits for table load to complete.


        send_scrapper_result_to_bigquery(bq_client, table_ref, job_config, item)


app = webapp2.WSGIApplication([
    ('/send_bq', BigQueryHandler)
], debug=True)
# [END all]