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

def get_bq_scrapertext(dataset, table):
    bq_client = bigquery.Client()
    table_ref = bq_client.dataset(dataset).table(table)
    iterator = bq_client.list_rows(table_ref, selected_fields=[bigquery.SchemaField('TEXT', 'STRING')])
    rows = list(iterator)

    return rows


def save_sentiment_result_to_bq(dataset_selected, table_selected, sentiment_result):
    bq_client = bigquery.Client()
    dataset_ref = bq_client.dataset(dataset_selected)

     # [START create_table for sentiment result]
    SCHEMA = [
        bigquery.SchemaField('TEXT', 'STRING'),
        bigquery.SchemaField('SCORE', 'STRING'),
        bigquery.SchemaField('MAGNITUDE', 'STRING'),
    ]
    table_ref = dataset_ref.table(str(table_selected) + '_' + 'sentiment_result')
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = bq_client.create_table(table)      # API request

    # [END create_table]

    # [START table_insert_rows]
    row_to_insert_text = [
        (u'Phred Phlyntstone', '21', '45')
    ]
    
    bq_client.insert_rows(table, row_to_insert_text)  # API request

    #logging.info('ERRORS: ' + str(errors))

    # [END table_insert_rows]





