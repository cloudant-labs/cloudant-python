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

    def __iter__(self, **kwargs):
        response = self.get(stream=True, **kwargs)
        # block until result if the object is using async
        if hasattr(response, 'result'):
            response = response.result()
        for line in response.iter_lines():
            line = line.decode('utf-8')
            if line:
                if line[-1] == ',':
                    line = line[:-1]
                try:
                    yield json.loads(line)
                except (TypeError, ValueError):
                    # if we can't decode a line, ignore it
                    pass

    def iter(self, **kwargs):
        """
        Like the magic method `__iter__`, but allows you to
        pass query parameters, like so:

            view = db.view('...')
            options = {
                'key': 'thegoodstuff',
                'include_docs': True
            }
            for row in view.iter(params=options):
                # emits only rows with the key 'thegoodstuff'
                # with each row's emitting document
        """
        return self.__iter__(**kwargs)
