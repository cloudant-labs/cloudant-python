from .resource import Resource
from .document import Document
from .design import Design
from .index import Index


class Database(Resource):

    """
    Connection to a specific database.

    Learn more about the raw API from the [Cloudant docs](http://docs.cloudant.com/api/database.html).
    """

    def document(self, name, **kwargs):
        """
        Create a `Document` object from `name`.
        """
        opts = dict(self.opts.items() + kwargs.items())
        return Document(self._make_url(name), session=self._session, **opts)

    def design(self, name, **kwargs):
        """
        Create a `Design` object from `name`, like so:

            db.design('test')
            # refers to DB/_design/test
        """
        opts = dict(self.opts.items() + kwargs.items())
        return Design(self._make_url('/'.join(['_design', name])), session=self._session, **opts)

    def __getitem__(self, name):
        """Shortcut to `Database.document`."""
        return self.document(name, **self.opts)

    def __setitem__(self, name, doc):
        """Creates `doc` with an ID of `name`."""
        response = self.put(name, params=doc)
        # block until result if the object is using async
        if hasattr(response, 'result'):
            response = response.result()
        response.raise_for_status()

    def all_docs(self, **kwargs):
        """
        Return an `Index` object referencing all documents in the database.
        You can treat it like an iterator:

            for doc in db.all_docs():
                print doc
        """
        return Index(self._make_url('_all_docs'), session=self._session, **kwargs)

    def __iter__(self):
        """Formats `Database.all_docs` for use as an iterator."""
        return self.all_docs().__iter__()

    def bulk_docs(self, *docs, **kwargs):
        """
        Save many docs, all at once. Each `doc` argument must be a dict, like this:

                db.bulk_docs({...}, {...}, {...})
                # saves all documents in one HTTP request

        For more detail on bulk operations, see
        [Creating or updating multiple documents](http://docs.cloudant.com/api/database.html#creating-or-updating-multiple-documents)
        """
        params = {
            'docs': docs
        }
        return self.post('_bulk_docs', params=params, **kwargs)

    def changes(self, **kwargs):
        """
        Gets a list of the changes made to the database.
        This can be used to monitor for update and modifications to the database
        for post processing or synchronization.

        Automatically adjusts the request to handle the different response behavior
        of polling, longpolling, and continuous modes.

        For more information about the `_changes` feed, see
        [the docs](http://docs.cloudant.com/api/database.html#obtaining-a-list-of-changes).
        """
        if 'params' in kwargs:
            if 'feed' in kwargs['params']:
                if kwargs['params']['feed'] == 'continuous':
                    kwargs['stream'] = True

        return self.get('_changes', **kwargs)

    def missing_revs(self, revs, **kwargs):
        """
        Refers to [this method](http://docs.cloudant.com/api/database.html#retrieving-missing-revisions).
        """
        return self.post('_missing_revs', params=revs, **kwargs)

    def revs_diff(self, revs, **kwargs):
        """
        Refers to [this method](http://docs.cloudant.com/api/database.html#retrieving-differences-between-revisions)
        """
        return self.post('_revs_diff', params=revs, **kwargs)

    def view_cleanup(self, **kwargs):
        """
        Cleans up the cached view output on disk for a given view. For example:

            print db.view_cleanup().result().json()
            # {'ok': True}
        """
        return self.post('_view_cleanup', **kwargs)
