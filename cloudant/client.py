# coding=utf-8
import requests


class Client(object):

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password


    def get_all_dbs(self):
        r = requests.get('{}/_all_dbs'.format(self.base_url), auth=(self.username, self.password))
        if r.ok:
            return r.json()
        return []

    def get_database_info(self, db_name):
        r = requests.get('{}/{}'.format(self.base_url, db_name), auth=(self.username, self.password))
        return r.json()

    def create_database(self, db_name):
        r = requests.put('{}/{}'.format(self.base_url, db_name), auth=(self.username, self.password))
        return r.json()

    def delete_database(self, db_name):
        r = requests.delete('{}/{}'.format(self.base_url, db_name), auth=(self.username, self.password))
        return r.json()
