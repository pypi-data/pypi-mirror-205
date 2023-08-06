import logging

import requests

logger = logging.getLogger(__name__)


class Retriever:

    def __init__(self, url):
        self.url = url

    def retrieve(self):
        print(f"retrieving {self.url}")
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text
