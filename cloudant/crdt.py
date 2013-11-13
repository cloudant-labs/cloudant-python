"""
The CloudantSet knows:

 * it's state on the database
 * the additions it's had locally
 * the deletions it's had locally
 * how to write its self to the database

It is implemented by using a frozeset (external state) and two normal sets (one
each for add/delete) and an Index pointing at the view that aggregates state in
the database.

If it works out someone using this class should just care about the values they
add/remove, and the class will take care of the rest.
"""

# from .index import Index


class CloudantSetFactory():
    """
    This sets up a view and a CRDT object for that view.
    """
    pass


class CloudantSet():
    def __init__(self, name, index, database):
        self.index = index
        self.database = database
        self.get_external_state()
        self.increments = set()
        self.decrements = set()
        self.name = name

    def get_external_state(self):
        # TODO: query self.index
        result = ['a', 'b', 'c']
        self.external_state = frozenset(result)

    def add(self, item):
        self.increments.add(item)

    def remove(self, item):
        self.decrements.add(item)

    def persist(self):
        """
        Write the necessary documents to the database.
        """
        docs = [
            {"name": self.name, "value": x, "type": "increment"}
            for x in self.increments
        ]
        docs.extend([
            {"name": self.name, "value": x, "type": "decrement"}
            for x in self.decrements
        ])
        self.database.save_docs(*docs)
        # TODO: Make this optional?
        self.get_external_state()
        # This should do some error handling, maybe?
        self.increments = set()
        self.decrements = set()

    def __iter__(self):
        """
        Do the set operation and return the iterable over the result
        """
        return iter(
            self.external_state.union(self.increments) - self.decrements
        )

    def __str__(self):
        return str(
            self.external_state.union(self.increments) - self.decrements
        )


class CloudantNumericCounter:
    def __init__(self, name, index, database):
        self.index = index
        self.database = database
        self.get_external_state()
        self.increment = 0
        self.decrement = 0
        self.name = name

    def get_external_state(self):
        # TODO: query self.index
        result = 10
        self.count = result

    def add(self, value):
        return self + value

    def remove(self, value):
        return self - value

    def persist(self):
        """
        Write the necessary documents to the database.
        """
        docs = [
            {"name": self.name, "value": self.increment},
            {"name": self.name, "value": self.decrement}
        ]
        self.database.save_docs(*docs)
        self.get_external_state()
        self.increments = []
        self.decrements = []

    def __abs__(self):
        """
        Do the set operation and return the iterable over the result
        """
        return self.count + self.increment + self.decrement

    def __repr__(self):
        return "%s" % self.__abs__()

    def __add__(self, value):
        self.increment += value
        return self

    def __sub__(self, value):
        self.decrement -= value
        return self
