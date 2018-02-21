# Import the Google Cloud BigQuery Library
from google.cloud import bigquery
from google.cloud.bigquery import Dataset

import os
import logging
logging.basicConfig(level=logging.DEBUG)

from io import StringIO


def send_scrapper_result_to_bigquery(data):
    
    dataset_name = 'sentimentcrawlerdataset'
    table_id = 'scrapper_table'
        
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_id)
    
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'NEWLINE_DELIMITED_JSON'
    job_config.autodetect = True

    #load_job = bigquery_client.load_table_from_uri('https://storage.cloud.google.com' + source_file_name, table_ref, job_config=job_config)  # API request
    load_job = bigquery_client.load_table_from_file(StringIO(unicode(data)), table_ref, job_config=job_config) # API request

    load_job.result()  # Waits for table load to complete.
