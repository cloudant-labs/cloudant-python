#!/usr/bin/env python
# coding=utf-8

from unittest import TestCase
from cloudant.client import Client
from cloudant.errors import PermissionsError


class ClientTestCases(TestCase):
    """
    Tests for the Cloudant client
    """

    def setUp(self):
        """
        Set the client up for testing
        """
        self.base_url = 'https://dustinmm80.cloudant.com'
        self.client = Client(self.base_url, username='peciderelfwairselystredy', password='aI8MpQ2XtWXqDCL1wg1jNoTF')
        self.db_name = 'test'

    def test_get_all_dbs(self):
        """
        Call to get all databases raises permissions error for test user
        """
        with self.assertRaises(PermissionsError):
            self.client.get_all_dbs()

    def test_create_database(self):
        """
        Call to create a database raises permissions error for test user
        """
        with self.assertRaises(PermissionsError):
            self.client.create_database('new database')

    def test_get_database_info(self):
        """
        Getting database info works if you have read rights, otherwise throws PermissionsError
        """
        info = self.client.get_database_info(self.db_name)
        self.assertNotEqual(info, '')

        with self.assertRaises(PermissionsError):
            self.assertEqual(self.client.get_database_info('crud'), '')

    def test_delete_database(self):
        """
        Call to delete a database raises permissions error for test user
        """
        with self.assertRaises(PermissionsError):
            self.client.create_database(self.db_name)
