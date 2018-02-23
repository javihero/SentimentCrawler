#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apiclient.discovery import build
from natural_config import API_KEY


class NaturalService():
    """
    Natural Language API calls are made from here
    """

    service = build('language', 'v1',
                    developerKey=API_KEY)
    collection = service.documents()

    def request_sentiment(self, text):
        """
        Returns text, overall score and magnitude, and a dict with each sentence, specific score and magnitude
        """

        data = {}
        data['document'] = {}
        data['document']['language'] = 'es'
        data['document']['content'] = text
        data['document']['type'] = 'PLAIN_TEXT'

        request = self.collection.analyzeSentiment(body=data)
        sentiment = request.execute()

        result = {}
        result['text'] = text
        result['score'] = sentiment['documentSentiment']['score']
        result['magnitude'] = sentiment['documentSentiment']['magnitude']
        result['sentences'] = sentiment['sentences']

        return result
