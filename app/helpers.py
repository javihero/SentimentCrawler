import json
from google.appengine.api import taskqueue, urlfetch


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


def send_to_bq_task(item):
    taskqueue.add(url='/send_bq', target='worker', params=item)
