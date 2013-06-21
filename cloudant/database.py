#!/usr/bin/env python
# coding=utf-8
from itertools import chain
import json
from urllib import urlencode
from cloudant.document import Document


class Database(object):
    """
    Cloudant database
    """

    def __init__(self, name, client):
        """
        Initializes a database by sending a request to the Cloudant service

        :param name: Name of the database
        :param client: Client used to connect to the service
        """
        response = client.get_database_info(name)
        self.name = name

        self.client = client
        if response and isinstance(response, dict):
            for key, value in response.items():
                if key == 'db_name':
                    key = 'name'
                setattr(self, key, value)
        else:
            raise ValueError('{} is not a valid database'.format(name))

    def get_all_documents(self, include_docs=True, **kwargs):
        """
        Get all documents in the database

        :param include_docs: Include the full content of the documents in the return

        :param kwargs: can include ::

            descending      :bool:      Return the documents in descending by key order: False
            endkey          :string:    Stop returning records when the specified key is reached
            endkey_docid    :string:    Stop returning records when the specified document ID is reached
            group           :bool:      Group the results using the reduce function to a group or single row: False
            group_level     :int:       Specify the group level to be used
            include_docs    :bool:      Include the full content of the documents in the return: False
            inclusive_end   :bool:      Specifies whether the specified end key should be included in the result: True
            key             :string:    Return only documents that match the specified key
            limit           :int:       Limit the number of the returned documents to the specified number
            reduce          :bool:      Use the reduction function: True
            skip            :int:       Skip this number of records before starting to return the results: 0
            stale           :string:    Allow the results from a stale view to be used: '', 'ok'
            startkey        :string:    Return records starting with the specified key
            startkey_docid  :string:    Return records starting with the specified document ID

        :return: List of Document objects
        """
        kwargs['include_docs'] = include_docs

        for kwarg, value in kwargs.items():
            kwargs[kwarg] = str(value).lower()

        r = self.client.get('/{}/_all_docs'.format(self.name), params=urlencode(kwargs))

        if r.ok:
            r_json = r.json()


            return [Document(x) for x in r_json['rows']]
        return []

    def get_document(self, _id, **kwargs):
        """
        Retrieve a document from the database

        :param id: ID of the document to retrieve

        :param kwargs: can include ::

            conflicts   :bool:      Returns the conflict tree for the document.
            rev         :string:    Specify the revision to return
            revs        :bool:      Return a list of the revisions for the document
            revs_info   :bool:      Return a list of detailed revision information for the document

        :return: Document retrieved from the database
        """
        r = self.client.get('/{}/{}'.format(self.name, _id), params=urlencode(kwargs))

        if r.status_code == 200:
            return Document(r.json())

    def create_document(self, **kwargs):
        """
        Creates or updates a document in the database

        :param kwargs: can include ::

            batch   :string:        Allow document store request to be batched with others: '', 'ok'

        :return: The created or updated Document
        """
        json_kwargs = json.dumps(kwargs)
        r = self.client.post('/{}'.format(self.name), data=json_kwargs, headers={'content-type': 'application/json'})

        if r.status_code == 201:
            return_kwargs = json.loads(json.dumps(r.json()))
            return Document(dict(chain(kwargs.iteritems(), return_kwargs.iteritems())))

        elif r.status_code == 409:
            raise KeyError('Document already exists in the database')

    def delete_document(self, _id, _rev):
        """
        Delete a revision of a document

        :param _id: Document ID
        :param _rev: Current revision of the document for validation
        :return: Boolean for success or failure
        """
        r = self.client.delete('/{}/{}'.format(self.name, _id), params={'rev':_rev})

        return r.ok
