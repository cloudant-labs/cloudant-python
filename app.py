import requests
import json

class Resource(object):
  """
  REST resource class: implements GET, POST, PUT, DELETE methods
  and stores options to pass to requests
  """
  def __init__(self, **kwargs):
    self._set_options(**kwargs)

    for method in ['get', 'post', 'put', 'delete']:
      setattr(self, method, self._make_request(method))

  def _set_options(self, **kwargs):
    self.opts = {
      'headers': {
        'Content-Type': 'application/json',
        'Accept':       'application/json'
      }
    }
    if kwargs:
      self.opts.update(kwargs)

  def _make_url(self, path=''):
    """Joins the uri, optional database name, and optional path"""
    parts = [self.uri]
    if hasattr(self, 'name'): 
      parts.append(getattr(self, 'name', ''))
    if path: 
      parts.append(path)
    return '/'.join(parts)

  def _make_request(self, method, make_path=None):
    def inner(path='', **kwargs):
      kwargs.update(self.opts)
      # normalize `params` kwarg according to method
      if method in ['post', 'put']:
        if 'params' in kwargs:
          kwargs['data'] = json.dumps(kwargs['params'])
          del kwargs['params']
      # `make_path` changes `path` according to any special needs
      if make_path:
        path = make_path(path)
      return getattr(requests, method)(self._make_url(path), **kwargs)
    return inner

class Attachment(Resource):
  """
  Attachment methods for a single document
  """
  def __init__(self, uri, name, doc, **kwargs):
    self.uri = uri
    self.name = name
    self.doc = doc
    super(Attachment, self)._set_options(**kwargs)

    def _make_path(path=''):
      return '/'.join([self.doc, 'attachment', path])

    for method in ['get', 'put', 'delete']:
      setattr(self, method, self._make_request(method, _make_path))

class View(Resource):
  """
  Methods for design documents
  """
  def __init__(self, uri, name, doc, **kwargs):
    self.uri = uri
    self.name = name
    self.doc = doc
    super(View, self).__init__(**kwargs)

    def _make_path(path=''):
      return '/'.join(['_design', self.doc, path])

    for method in ['get', 'put', 'delete']:
      setattr(self, method, self._make_request(method, _make_path))

  def query(self, viewname, **kwargs):
    path = '/'.join(['_view', viewname])
    self.get(path, **kwargs)

class Database(Resource):
  """
  Connection to a specific database
  """
  def __init__(self, uri, name, **kwargs):
    self.uri = uri
    self.name = name
    super(Database, self).__init__(**kwargs)

  def Attachment(self, doc, **kwargs):
    return Attachment(self.uri, self.name, doc, **kwargs)

  def View(self, doc, **kwargs):
    return View(self.uri, self.name, doc, **kwargs)

  def merge(self, docname, change, **kwargs):
    """
    Get document, merge changes, put updated document
    """
    doc = self.get(docname).json()
    doc.update(change)
    return self.put(docname, params=doc)

  def getOrCreate(self, docname='', **kwargs):
    """
    Get; if nothing is found, post (doc) or put (db)
    """
    remote_doc = self.get(docname).json()
    if 'error' in doc and doc['error'] == "not_found":
      # create a new document
      if docname:
        return self.post(docname, **kwargs)
      # create a new database
      else:
        return self.put()
    # return the found doc
    else:
      return remote_doc

class Connection(Resource):
  def __init__(self, uri="http://localhost:5984", **kwargs):
    self.uri = uri
    super(Connection, self).__init__(**kwargs)

  def Database(self, name, **kwargs):
    return Database(self.uri, name, **kwargs)