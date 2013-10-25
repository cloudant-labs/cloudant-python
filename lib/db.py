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

    def attachment(self, docname, **kwargs):
        """
        Create an `Attachment` object from `docname` and the settings
        for the current database.
        """
        return Attachment(self.uri, self.name, docname, **kwargs)

    def view(self, docname, **kwargs):
        """
        Create a `View` object from `docname` and the settings
        for the current database.
        """
        return View(self.uri, self.name, docname, **kwargs)

    def merge(self, docname, change, **kwargs):
        """
        Get document by `docname`, merge `changes`, 
        and then `PUT` the updated document back to the server
        """
        doc = self.get(docname).json()
        doc.update(change)
        return self.put(docname, params=doc, **kwargs)

    def get_or_create(self, doc=None, **kwargs):
        """
        Given a document with an _id attribute, returns it if it exists.

        If it doesn't, it tries to create it.

        If the doc is None, it tries to get or create the current database instead.
        """
        if doc:
            res = self.get(doc['_id'])
        else:
            res = self.get()

        res_json = res.json()
        if 'error' in res_json and res_json['error'] == "not_found":
            # create a new document
            if docname:
                if '_id' not in doc:
                    doc['_id'] = docname
                return self.post(docname, params=doc, **kwargs)
            # create a new database
            else:
                return self.put()
        # return the found doc
        else:
            return res

    def changes(self, **kwargs):
        """
        Gets a list of the changes made to the database. This can be used to monitor for update and modifications to the database for post processing or synchronization.

        Automatically adjusts the request to handle the different response behavior of polling, longpolling, and continuous modes.
        """
        if 'params' in kwargs:
            if 'feed' in kwargs['params']:
                if kwargs['params']['feed'] == 'continuous':
                    kwargs['stream'] = True
        print kwargs
        return self.get('_changes', **kwargs)
