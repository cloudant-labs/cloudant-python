from .rest import Resource


class Attachment(Resource):

    """
    Attachment methods for a single document
    """
    def __init__(self, uri, name, doc, **kwargs):
        self.uri = uri
        self.name = name
        self.doc = doc
        super(Attachment, self)._set_options(**kwargs)

        def _make_path(path=''):
            return '/'.join([self.doc, 'attachment', path])

        for method in ['get', 'put', 'delete']:
            setattr(self, method, self._make_request(method, _make_path))
