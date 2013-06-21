#!/usr/bin/env python
# coding=utf-8

class PermissionsError(Exception):

    def __init__(self, *args, **kwargs):
        super(PermissionsError, self).__init__(*args, **kwargs)
