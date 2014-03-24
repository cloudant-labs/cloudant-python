from .document import Document
from .index import Index

class Design(Document):
    """
    Connection to a design document, which stores custom indexes and other database functions.

    Learn more about design documents from the [Cloudant docs](http://docs.cloudant.com/api/design.html)
    """


    def index(self, path, **kwargs):
        """
        Create a `Index` object referencing the function at `path`. For example:

            index = doc.index('_view/index-name')
            # refers to /DB/_design/DOC/_view/index-name
        """
        opts = dict(self.opts, **kwargs)
        return Index(self._make_url(path), session=self._session, **opts)

    def view(self, function, **kwargs):
        """
        Create a `Index` object referencing the secondary index at `_view/{function}`. For example:

            index = doc.view('index-name')
            # refers to /DB/_design/DOC/_view/index-name

        For more on secondary indices, see
        [Querying a View](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)
        """
        return self.index('/'.join(['_view', function]), **kwargs)

    def search(self, function, **kwargs):
        """
        Creates a `Index` object referencing the search index at `_search/{function}`. For example:

            index = doc.search('index-name')
            # refers to /DB/_design/DOC/_search/search-name

        For more details on search indexes, see
        [Searching for documents using Lucene queries](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)
        """
        return self.index('/'.join(['_search', function]), **kwargs)

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
