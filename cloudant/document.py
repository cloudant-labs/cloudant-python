from .resource import Resource
from .attachment import Attachment


class Document(Resource):

    """
    Connection to a specific document.

    Learn more about the raw API from the [Cloudant docs](http://docs.cloudant.com/api/documents.html)
    """

    def attachment(self, name, **kwargs):
        """
        Create an `Attachment` object from `name` and the settings
        for the current database.
        """
        opts = dict(self.opts.items() + kwargs.items())
        return Attachment(self._make_url(name), session=self._session, **opts)

    def merge(self, change, **kwargs):
        """
        Merge `change` into the document,
        and then `PUT` the updated document back to the server.
        """
        doc = self.get().result().json()
        doc.update(change)
        return self.put(params=doc, **kwargs)

    def delete(self, rev, **kwargs):
        """
        Delete the given revision of the current document. For example:

            rev = doc.get().result().json()['_rev']
            doc.delete(rev)
        """
        return super(Document, self).delete(params={'rev': rev}, **kwargs)
