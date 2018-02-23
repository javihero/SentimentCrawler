import urllib2

import json
import cloudstorage as gcs
from google.appengine.api import taskqueue

#[START retries]
my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]



def sanitize_url(old_url):
    if not old_url.startswith(('http://', 'https://')):
        new_url = 'http://' + old_url
        return new_url
    else:
        return old_url


def request_scrapy(api_url):
    content = urllib2.urlopen(api_url).read()
    json_content = json.loads(content)
    return json_content['items']

"""
def send_to_gstorage(self, filename, content):
    self.tmp_filenames_to_clean_up = []
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    gcs_file = gcs.open(filename,
                        'w',
                        content_type='text/plain',
                        options={'x-goog-meta-foo': 'foo',
                                 'x-goog-meta-bar': 'bar'},
                        retry_params=write_retry_params)
    gcs_file.write(str(content))
    gcs_file.close()
    self.tmp_filenames_to_clean_up.append(filename)
"""   

def send_to_bq_task(bq_client, table_ref, job_config, item):
        taskqueue.add(url='/send_bq', target='worker', params={'bq_client': bq_client, 'table_ref': table_ref, 'job_config': job_config, 'item': item})

