# coding=utf-8
from urllib import urlencode
import requests

VALID_KWARGS = [
    'descending',
    'endkey',
    'endkey_docid',
    'group',
    'group_level',
    'include_docs',
    'inclusive_end',
    'key',
    'reduce',
    'skip',
    'stale',
    'startkey',
    'startkey_docid'
]

class Database(object):

    def __init__(self, name, client):
        self.name = name
        self.client = client

    def get_all_documents(self, **kwargs):
        for kwarg, value in kwargs.items():
            if kwarg in VALID_KWARGS:
                kwargs[kwarg] = str(value).lower()
            else:
                kwargs.pop(kwarg)

        r = requests.get(
            '{}/{}/_all_docs'.format(self.client.base_url, self.name),
            auth=(self.client.username, self.client.password),
            params=urlencode(kwargs)
        )
        if r.ok:
            return r.json()['rows']
        return []
