from .rest import Resource
from .db import Database


class Connection(Resource):

    def __init__(self, uri="http://localhost:5984", **kwargs):
        self.uri = uri
        super(Connection, self).__init__(**kwargs)

    def database(self, name, **kwargs):
        return Database(self.uri, name, **kwargs)
