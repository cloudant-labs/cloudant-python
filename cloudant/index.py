from .resource import Resource
import json


class Index(Resource):

    """
    Methods for design document indexes.
    Different kinds of indexes will behave differently, so here are helpful docs:

    * [Lucene search indexes](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)
    * [Secondary indexes / "views"](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)

    Then, you just use basic HTTP methods to perform queries, like this:

        index.get(params=QUERY_ARGUMENTS)

    Remember, before you can query an index, you have to make sure it's in your database.
    See [these docs](http://docs.cloudant.com/api/design-documents-get-put-delete-copy.html#creating-or-updating-a-design-document)
    for how to do that.
    """

    def __iter__(self):
        response = self.get(stream=True).result()
        for line in response.iter_lines():
            if line:
                if line[-1] == ',':
                    line = line[:-1]
                try:
                    yield json.loads(line)
                except ValueError:
                    # if we can't decode a line, ignore it
                    pass