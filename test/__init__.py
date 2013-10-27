import lib as divan
import unittest
import os


class ResourceTest(unittest.TestCase):

    def setUp(self):
        self.uri = 'http://localhost:5984'
        self.db_name = 'testdb'
        self.otherdb_name = 'othertestdb'
        self.doc_name = 'testdoc'
        self.otherdoc_name = 'othertestdoc'


class ConnectionTest(ResourceTest):

    def setUp(self):
        super(ConnectionTest, self).setUp()
        self.conn = divan.Connection(self.uri)

    def testInfo(self):
        self.conn.info()

    def testAllDbs(self):
        self.conn.all_dbs()

    def testCreateDb(self):
        self.conn.database(self.db_name)
        self.conn[self.db_name]

    def testUuids(self):
        self.conn.uuids()


class DatabaseTest(ResourceTest):

    def setUp(self):
        super(DatabaseTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))

    def testCrud(self):
        """
        Create, read, and delete a database
        """
        r = self.db.put()
        assert r.status_code == 201
        r = self.db.get()
        assert r.json()['db_name'] == self.db_name
        r = self.db.delete()
        assert r.status_code == 200


class DocumentTest(ResourceTest): pass
class AttachmentTest(ResourceTest): pass
class ViewTest(ResourceTest): pass

if __name__ == "__main__":
    unittest.main()
