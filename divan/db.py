from .rest import Resource
from .view import View
from .attach import Attachment


class Database(Resource):

    """
    Connection to a specific database
    """
    def __init__(self, uri, name, **kwargs):
        self.uri = uri
        self.name = name
        super(Database, self).__init__(**kwargs)

    def attachment(self, doc, **kwargs):
        return Attachment(self.uri, self.name, doc, **kwargs)

    def view(self, doc, **kwargs):
        return View(self.uri, self.name, doc, **kwargs)

    def merge(self, docname, change, **kwargs):
        """
        Get document, merge changes, put updated document
        """
        doc = self.get(docname).json()
        doc.update(change)
        return self.put(docname, params=doc)

    def get_or_create(self, docname='', **kwargs):
        """
        Get; if nothing is found, post (doc) or put (db)
        """
        res = self.get(docname)
        doc = res.json()
        if 'error' in doc and doc['error'] == "not_found":
            # create a new document
            if docname:
                return self.post(docname, **kwargs)
            # create a new database
            else:
                return self.put()
        # return the found doc
        else:
            return res

    def bulk_docs(self, docs):
        return self.post('_bulk_docs', params={'docs': docs})
