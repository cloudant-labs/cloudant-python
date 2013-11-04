#!/usr/bin/env python
# coding=utf-8

from unittest import TestCase
from cloudant.client import Client
from cloudant.database import Database
from cloudant.errors import PermissionsError


def clear_database(db):
    """
    Clear all documents from a database
    :param db: Database object
    """
    docs = db.get_all_documents()
    for doc in docs:
        db.delete_document(doc.id, doc.rev)


class DatabaseTestCases(TestCase):
    """
    Tests for the Cloudant client
    """

    def setUp(self):
        """
        Set the client up for testing
        """
        self.base_url = 'https://dustinmm80.cloudant.com'
        self.client = Client(self.base_url, username='peciderelfwairselystredy', password='aI8MpQ2XtWXqDCL1wg1jNoTF')
        self.db = Database('test', self.client)
        clear_database(self.db)

    def tearDown(self):
        clear_database(self.db)

    def test_create_document(self):
        """
        Create a new document
        """
        doc = self.db.create_document(
            name='Route', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'}
        )

        self.assertEqual(doc.name, 'Route')
        self.assertEqual(len(self.db.get_all_documents()), 1)

    def test_get_all_documents(self):
        """
        Create some documents and retrieve them
        """
        self.db.create_document(name='Route1', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'})
        self.db.create_document(name='Route2', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'})
        self.db.create_document(name='Route3', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'})

        docs = self.db.get_all_documents()
        print(docs)
        self.assertEqual(len(docs), 3)

    def test_delete_document(self):
        """
        Test creating and deleting a document
        """
        doc = self.db.create_document(
            name='Route1', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'}
        )

        docs = self.db.get_all_documents()
        self.assertEqual(len(docs), 1)

        self.db.delete_document(doc.id, doc.rev)

        docs = self.db.get_all_documents()
        self.assertEqual(len(docs), 0)
