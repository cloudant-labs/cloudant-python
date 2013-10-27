from .resource import Resource
from .view import View
from .attachment import Attachment


class Document(Resource):

    def attachment(self, name, **kwargs):
        """
        Create an `Attachment` object from `name` and the settings
        for the current database.
        """
        return Attachment(self._make_url(name), session=self._session, **kwargs)

    def view(self, method, function, **kwargs):
        """
        Create a `View` object by joining `method` and `function`.
        """
        path = '/'.join([method, function])
        return View(self._make_url(path), session=self._session, **kwargs)

    def merge(self, change, **kwargs):
        """
        Merge `changes` into the document,
        and then `PUT` the updated document back to the server
        """
        doc = self.get().result().json()
        doc.update(change)
        return self.put(params=doc, **kwargs)

    def delete(self, rev, **kwargs):
        """
        Delete the given revision of the current document.
        """
        return super(Document, self).delete(params={'rev': rev}, **kwargs)