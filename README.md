# Sentiment crawler

## App
  This folder contains the web page that is deployed in App Engine, requires Python 2.7

  * 'dev_appserver app.yaml' to serve in localhost
  * 'gcloud app deploy' to submit changes to App Engine
  * Twitter and Natural Language API have both gitignored config files with keys (put your own)

## Scrapper
  This folder contains the Scrapy project (crawlers), requires Python 3

  * 'scrapyrt' to serve an API on localhost:9080
  * URL format is -> 'http://localhost:9080/crawl.json?spider_name=' + spider + '&url=' + url 