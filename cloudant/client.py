#!/usr/bin/env python
# coding=utf-8
import requests
from cloudant.database import Database
from cloudant.errors import PermissionsError


class Client(object):
    """
    Cloudant client, used to query service
    """

    def __init__(self, base_url, username, password):
        """
        Initializes a client

        :param base_url: Base Cloudant url
        :param username: Username of Cloudant user
        :param password: Password of Cloudant user
        """
        self.base_url = base_url
        self.auth = (username, password)

    def get(self, path, params=None, headers=None):
        """
        Generic GET request, in the client context

        :param path: Path for API, should always start with /
        :param params: URL parameters
        :param headers: HTTP headers
        :return: Response object
        """
        return requests.get(
            '{}{}'.format(self.base_url, path),
            params=params,
            headers=headers,
            auth=self.auth
        )

    def post(self, path, data=None, headers=None):
        """
        Generic POST request, in the client context

        :param path: Path for API, should always start with /
        :param data: HTTP body, dictionary
        :param headers: HTTP headers
        :return: Response object
        """
        return requests.post(
            '{}{}'.format(self.base_url, path),
            data=data,
            headers=headers,
            auth=self.auth
        )

    def put(self, path, headers=None):
        """
        Generic PUT request, in the client context

        :param path: Path for API, should always start with /
        :param headers: HTTP headers
        :return: Response object
        """
        return requests.put(
            '{}{}'.format(self.base_url, path),
            headers=headers,
            auth=self.auth
        )

    def delete(self, path, params=None, headers=None):
        """
        Generic DELETE request, in the client context

        :param path: Path for API, should always start with /
        :param params: URL parameters
        :param headers: HTTP headers
        :return: Response object
        """
        return requests.delete(
            '{}{}'.format(self.base_url, path),
            params=params,
            headers=headers,
            auth=self.auth
        )


    def get_all_dbs(self):
        """
        Retrieve all databases for this account

        :return: List of Database objects
        """
        r = self.get('/_all_dbs')

        if r.ok:
            r_json = r.json()
            return [Database(name, self) for name in r_json]

        elif r.status_code == 403:
            raise PermissionsError('No permissions to get all databases')

        return []

    def get_database_info(self, db_name):
        """
        Get information on the specified database

        :param db_name: Name of the database

        :return: Response JSON dictionary
        """
        r = self.get('/{}'.format(db_name))

        if r.ok:
            return r.json()
        elif r.status_code == 403:
            raise PermissionsError('No permissions to view database info')
        else:
            raise KeyError('Database not found')

    def create_database(self, db_name):
        """
        Create a database for this account

        :param db_name: Name of the database
        :return: Created Database object
        """
        r = self.put('/{}'.format(db_name))

        if r.ok or r.status_code == 412:
            return Database(name=db_name, client=self)

        elif r.status_code == 413:
            raise KeyError('Invalid database name')

        elif r.status_code == 403:
            raise PermissionsError('No permissions to create a database')

    def delete_database(self, db_name):
        """
        Delete a database on this account

        :param db_name: Name of the database
        :return: Boolean for success or failure
        """
        r = self.delete('/{}'.format(db_name))

        if r.ok:
            return True

        elif r.status_code == 403:
            raise PermissionsError('No permissions to delete a database')

