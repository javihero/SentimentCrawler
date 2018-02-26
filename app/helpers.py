import json
from google.appengine.api import taskqueue, urlfetch

# Import the Google Cloud BigQuery Library
from google.cloud import bigquery
from google.cloud.bigquery import Dataset

def sanitize_url(old_url):
    if not old_url.startswith(('http://', 'https://')):
        new_url = 'http://' + old_url
        return new_url
    else:
        return old_url


def request_scrapy(api_url):
    urlfetch.set_default_fetch_deadline(60)
    content = urlfetch.fetch(api_url).content
    json_content = json.loads(content)
    return json_content['items']


def send_to_bq_task(bq_client, table_ref, job_config, item):
        taskqueue.add(url='/send_bq', target='worker', params={'bq_client': bq_client, 'table_ref': table_ref, 'job_config': job_config, 'item': item})

def get_dict_datasets_tables():
    bq_client = bigquery.Client()
    datasets = bq_client.list_datasets() # API request(s)
    dict_datasets_tables = {}
    for single_dataset in datasets:
        dataset = bigquery.Dataset(bq_client.dataset(single_dataset.dataset_id))
        dataset_tables = bq_client.list_dataset_tables(dataset)
        dict_datasets_tables[single_dataset.dataset_id] = []
        for dataset_table in dataset_tables:
            dict_datasets_tables[single_dataset.dataset_id].append(dataset_table.table_id)
        
    return dict_datasets_tables