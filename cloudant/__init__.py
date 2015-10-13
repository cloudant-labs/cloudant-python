from .resource import Resource
from .account import Account
from .database import Database
from .document import Document
from .design import Design
from .attachment import Attachment
from .index import Index

import warnings
message = """You are using version 0.5.10 of this library,
             which is now deprecated. It will be replaced 
             with version 2.0.0 in early 2016. This will 
             introduce breaking changes. Please upgrade as
             soon as possible. Find out more at 
             https://github.com/cloudant/python-cloudant
          """

#we don't use DeprecationWarning because that message is ignored by default
warnings.warn(message) 
