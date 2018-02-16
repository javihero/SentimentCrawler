# Import the Google Cloud BigQuery Library
from google.cloud import bigquery


def send_result_to_bq(source_file_name):

    dataset_name = 'sentiment'
    table_id = 'quotes_table'

    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_id)

    with open(source_file_name, 'rb') as source_file:
        # This example uses CSV, but you can use other formats.
        # See https://cloud.google.com/bigquery/loading-data
        job_config = bigquery.LoadJobConfig()
        # job_config.source_format = 'text/json'
        job_config.source_format = 'NEWLINE_DELIMITED_JSON'
        job_config.autodetect = True

        job = bigquery_client.load_table_from_file(
            source_file, table_ref, job_config=job_config)

    job.result()  # Waits for job to complete

    print('Loaded {} rows into {}:{}.'.format(
        job.output_rows, dataset_name, table_id))
