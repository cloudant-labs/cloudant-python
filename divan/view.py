from .resource import Resource


class View(Resource):

    """
    Methods for design document indexes and special methods.
    Different kinds of indexes / methods will behave differently, so here are helpful docs:

    * [Lucene search indexes](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)
    * [Secondary indexes / "views"](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)
    * [List functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-list-functions)
    * [Show functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-show-functions)

    Then, you just use basic HTTP methods to perform queries, like this:

        view.get(params=QUERY_ARGUMENTS)

    Remember, before you can query an index, you have to make sure it's in your database.
    See [these docs](http://docs.cloudant.com/api/design-documents-get-put-delete-copy.html#creating-or-updating-a-design-document)
    for how to do that.
    """

    def __iter__(self):
        # allow indexes to be used as iterators
        return self.get().result().json()['rows'].__iter__()
