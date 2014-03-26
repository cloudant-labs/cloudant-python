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
        opts = dict(self.opts, **kwargs)
        return Attachment(self._make_url(name), session=self._session, **opts)

    def merge(self, change, **kwargs):
        """
        Merge `change` into the document,
        and then `PUT` the updated document back to the server.
        """
        response = self.get()
        # block until result if the object is using async/is a future
        if hasattr(response, 'result'):
            response = response.result()

        # handle upserts
        if response.status_code == 404:
            doc = {}
        else:
            response.raise_for_status()
            doc = response.json()

        # merge!
        doc.update(change)
        return self.put(params=doc, **kwargs)

    def delete(self, rev, **kwargs):
        """
        Delete the given revision of the current document. For example:

            rev = doc.get().result().json()['_rev']
            doc.delete(rev)
        """
        return super(Document, self).delete(params={'rev': rev}, **kwargs)

    def __del__(self):
        """
        Shortcut to synchronously deleting the document from the database.
        For example:

            del db['docKey']
        """
        response = self.get()
        # block until result if the object is using async/is a future
        if hasattr(response, 'result'):
            response = response.result()
        response.raise_for_status()
        doc = response.json()
        deletion = self.delete(self, doc['_rev'])
        # block until result if the object is using async/is a future
        if hasattr(deletion, 'result'):
            deletion = deletion.result()
        deletion.raise_for_status()
        