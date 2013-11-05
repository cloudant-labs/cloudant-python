from .resource import Resource
from .view import View
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

    def view(self, path, **kwargs):
        """
        Create a `View` object referencing the function at `path`. For example:

            view = doc.view('_view/index-name')
            # refers to /DB/_design/DOC/_view/index-name
        """
        opts = dict(self.opts.items() + kwargs.items())
        return View(self._make_url(path), session=self._session, **opts)

    def index(self, function, **kwargs):
        """
        Create a `View` object referencing the secondary index at `_view/{function}`. For example:

            view = doc.index('index-name')
            # refers to /DB/_design/DOC/_view/index-name

        For more on secondary indices, see
        [Querying a View](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)
        """
        return self.view('/'.join(['_view', function]), **kwargs)

    def search(self, function, **kwargs):
        """
        Creates a `View` object referencing the search index at `_search/{function}`. For example:

            view = doc.search('index-name')
            # refers to /DB/_design/DOC/_search/search-name

        For more details on search indexes, see
        [Searching for documents using Lucene queries](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)
        """
        return self.view('/'.join(['_search', function]), **kwargs)

    def list(self, function, index, **kwargs):
        """
        Make a GET request to the list function at `_list/{function}/{index}`. For example:

            future = doc.list('list-name', 'index-name')
            # refers to /DB/_design/DOC/_list/list-name/index-name

        For more details on list functions, see
        [Querying List Functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-list-functions).
        """
        return self.get(self._make_url('/'.join(['_list', function, index])), **kwargs)

    def show(self, function, id, **kwargs):
        """
        Make a GET request to the show function at `_show/{function}/{id}`. For example:

            future = doc.show('show-name', 'document-id')
            # refers to /DB/_design/DOC/_show/show-name/document-id

        For more details on show functions, see
        [Querying Show Functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-show-functions).
        """
        return self.get(self._make_url('/'.join(['_show', function, id])), **kwargs)

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
