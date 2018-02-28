# Import the Google Cloud BigQuery Library
from google.cloud import bigquery
from google.appengine.api import taskqueue

from io import StringIO
import random, string



def send_to_bq_task(bq_client, table_ref, job_config, item):
    taskqueue.add(url='/send_bq', target='worker', params={
                  'bq_client': bq_client, 'table_ref': table_ref, 'job_config': job_config, 'item': item})


def get_dict_datasets_tables():
    bq_client = bigquery.Client()
    datasets = bq_client.list_datasets()  # API request(s)
    dict_datasets_tables = {}
    for single_dataset in datasets:
        dataset = bigquery.Dataset(
            bq_client.dataset(single_dataset.dataset_id))
        dataset_tables = bq_client.list_dataset_tables(dataset)
        dict_datasets_tables[single_dataset.dataset_id] = []
        for dataset_table in dataset_tables:
            dict_datasets_tables[single_dataset.dataset_id].append(
                dataset_table.table_id)

    return dict_datasets_tables


def send_result_to_bigquery(dataset, table, data):

    bq_client = bigquery.Client()
    dataset_ref = bq_client.dataset(dataset)

    SCHEMA = [
        bigquery.SchemaField('TEXT', 'STRING')
    ]

    table_ref = dataset_ref.table(table)
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = bq_client.create_table(table)

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = 'NEWLINE_DELIMITED_JSON'
    job_config.autodetect = True

    # load_job = bigquery_client.load_table_from_uri('https://storage.cloud.google.com' + source_file_name, table_ref, job_config=job_config)  # API request
    load_job = bq_client.load_table_from_file(
        StringIO(unicode(data)), table_ref, job_config=job_config)  # API request

    load_job.result()  # Waits for table load to complete.


def get_bq_scrapertext(dataset, table):
    bq_client = bigquery.Client()
    table_ref = bq_client.dataset(dataset).table(table)
    iterator = bq_client.list_rows(table_ref, selected_fields=[
                                   bigquery.SchemaField('TEXT', 'STRING')])
    rows = list(iterator)

    return rows

def save_sentiment_result_to_bq(dataset_selected, table_selected):
    bq_client = bigquery.Client()
    dataset_ref = bq_client.dataset(dataset_selected)


    # [START create_table for sentiment result]
    SCHEMA = [
        bigquery.SchemaField('TEXT', 'STRING'),
        bigquery.SchemaField('SCORE', 'FLOAT'),
        bigquery.SchemaField('MAGNITUDE', 'FLOAT')
    ]
    random_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    table_ref = dataset_ref.table(str(table_selected) + '_' + 'sentiment_result_' + str(random_id))
    table = bigquery.Table(table_ref, schema=SCHEMA)
    table = bq_client.create_table(table)
    # [END create_table]

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = 'NEWLINE_DELIMITED_JSON'


    # Load sentiment result file from storage
    job = bq_client.load_table_from_uri('gs://urlbucket/sentiment_result.json', table_ref, job_config=job_config)
    job.result()





