import divan
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
        self.db.put()
        self.db.get()

    def testAllDocs(self):
        self.db.put()
        self.db.all_docs()

    def tearDown(self):
        self.db.delete()


class DocumentTest(ResourceTest):

    def setUp(self):
        super(DocumentTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))
        self.db.put()
        self.doc = self.db.document(self.doc_name)

    def testCrud(self):
        self.doc.put(params={
            'herp': 'derp'
            })
        self.doc.get()

    def tearDown(self):
        self.db.delete()


class AttachmentTest(ResourceTest): pass


class ViewTest(ResourceTest):

    def setUp(self):
        super(ViewTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))
        self.db.put()
        self.doc = self.db.document(self.doc_name)

    def testPrimaryIndex(self):
        """
        Show that views can be used as iterators
        """
        self.doc.put(params={
            'herp': 'derp'
            })
        for derp in self.db.all_docs():
            pass

    def tearDown(self):
        self.db.delete()


if __name__ == "__main__":
    unittest.main()
