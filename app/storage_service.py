# -*- coding: utf-8 -*-

#[START imports]
import cloudstorage as gcs
from google.appengine.api import app_identity
import os, json
import logging
logging.basicConfig(level=logging.DEBUG)
#[END imports]

#[START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]

def send_result_to_storage(self, data):
    bucket_name = 'urlbucket'
    bucket = '/' + bucket_name
    filename = bucket + '/sentiment_result.json'
    self.tmp_filenames_to_clean_up = []

    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/json',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    
    for text in data:
        for sentence in text['sentences']:
            sentence_row = {}
            sentence_row['TEXT'] = sentence['text']['content']
            sentence_row['SCORE'] = sentence['sentiment']['score']
            sentence_row['MAGNITUDE'] = sentence['sentiment']['magnitude']
            sentence_row = json.dumps(sentence_row)
            gcs_file.write(sentence_row + "\n")

    gcs_file.close()
    self.tmp_filenames_to_clean_up.append(filename)


def delete_sentiment_file(self):
    bucket_name = 'urlbucket'
    bucket = '/' + bucket_name
    filename = bucket + '/sentiment_result.json'
    gcs.delete(filename)
