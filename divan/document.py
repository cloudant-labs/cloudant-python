from .resource import Resource
from .view import View
from .attachment import Attachment


class Document(Resource):

    def attachment(self, name, **kwargs):
        """
        Create an `Attachment` object from `name` and the settings
        for the current database.
        """
        return Attachment(self._make_url(name), **kwargs)

    def view(self, method, function, **kwargs):
        """
        Create a `View` object by joining `method` and `function`.
        """
        path = '/'.join([method, function])
        return View(self._make_url(path), **kwargs)

    def merge(self, docname, change, **kwargs):
        """
        Get document by `docname`, merge `changes`,
        and then `PUT` the updated document back to the server
        """
        doc = self.get(docname).json()
        doc.update(change)
        return self.put(docname, params=doc, **kwargs)
