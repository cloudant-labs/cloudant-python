from .rest import Resource


class View(Resource):

    """
    Methods for design documents
    """
    def __init__(self, uri, name, doc, **kwargs):
        self.uri = uri
        self.name = name
        self.doc = doc
        super(View, self).__init__(**kwargs)

        def _make_path(path=''):
            return '/'.join(['_design', self.doc, path])

        for method in ['get', 'put', 'delete']:
            setattr(self, method, self._make_request(method, _make_path))

    def query(self, viewname, **kwargs):
        path = '/'.join(['_view', viewname])
        return self.get(path, **kwargs)
