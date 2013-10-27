from .resource import Resource


class View(Resource):

    """
    Methods for design documents
    """

    def __iter__(self):
        # allow indexes to be used as iterators
        return self.get().result().json()['rows'].__iter__()
