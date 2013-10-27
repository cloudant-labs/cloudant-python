from .resource import Resource
from .document import Document
from .view import View


class Database(Resource):

    """
    Connection to a specific database
    """

    def document(self, name, **kwargs):
        """
        Create a `Document` object from `name`.
        """
        return Document(self._make_url(name), session=self._session, **kwargs)

    def __getitem__(self, name):
        """Shortcut to `Database.document`."""
        return self.document(name)

    def __setitem__(self, name, doc):
        """Creates `doc` with an ID of `name`."""
        self.put(name, params=doc)

    def all_docs(self, **kwargs):
        """Return an iterator over all documents in the database."""
        return View(self._make_url('_all_docs'), session=self._session, **kwargs)

    def __iter__(self):
        """Formats `Database.all_docs` for use as an iterator."""
        return self.all_docs().__iter__()

    def save_docs(self, *docs, **kwargs):
        """
        Save many docs, all at once.
        """
        params = {
            'docs': docs
        }
        return self.post('_bulk_docs', params=params, **kwargs)

    def changes(self, **kwargs):
        """
        Gets a list of the changes made to the database. This can be used to monitor for update and modifications to the database for post processing or synchronization.

        Automatically adjusts the request to handle the different response behavior of polling, longpolling, and continuous modes.
        """
        if 'params' in kwargs:
            if 'feed' in kwargs['params']:
                if kwargs['params']['feed'] == 'continuous':
                    kwargs['stream'] = True

        return self.get('_changes', **kwargs)

    def missing_revs(self, revs, **kwargs):
        return self.post('_missing_revs', params=revs, **kwargs)

    def revs_diff(self, revs, **kwargs):
        return self.post('_revs_diff', params=revs, **kwargs)

    def view_cleanup(self, **kwargs):
        return self.post('_view_cleanup', **kwargs)
