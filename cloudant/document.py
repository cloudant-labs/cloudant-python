#!/usr/bin/env python
# coding=utf-8


class Document(object):
    """
    Document stored in the Cloudant database
    """

    def __init__(self, json):
        """
        Initializes a document from a dictionary

        :param json: Dictionary returned from the service
        """

        if 'doc' in json.keys():
            init_dict = json['doc']
        else:
            init_dict = json

        for key, value in init_dict.items():
            if key == '_id':
                key = 'id'
            if key == '_rev':
                key = 'rev'
            setattr(self, key, value)
