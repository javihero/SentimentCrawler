import urllib2
import json


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
