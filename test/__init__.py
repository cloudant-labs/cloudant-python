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

        self.test_doc = {
            'herp': 'derp',
            'name': 'Luke Skywalker'
        }
        self.test_otherdoc = {
            'derp': 'herp',
            'name': 'Larry, the Incorrigible Miscreant'
        }


class ConnectionTest(ResourceTest):

    def setUp(self):
        super(ConnectionTest, self).setUp()
        self.conn = divan.Connection(self.uri)

    def testInfo(self):
        self.conn.info()

    def testAllDbs(self):
        self.conn.all_dbs()

    def testSession(self):
        self.conn.session()

    def testActiveTasks(self):
        self.conn.active_tasks()

    def testReplicate(self):
        self.db = self.conn.database(self.db_name)
        self.db.put()
        self.conn.replicate(self.db_name, self.otherdb_name, params=dict(
            create_target=True))
        self.db.delete()
        self.conn.delete(self.otherdb_name)

    def testCreateDb(self):
        self.conn.database(self.db_name)
        self.conn[self.db_name]

    def testUuids(self):
        self.conn.uuids()


class DatabaseTest(ResourceTest):

    def setUp(self):
        super(DatabaseTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))
        self.db.put()

    def testGet(self):
        self.db.get()

    def testBulk(self):
        self.db.save_docs(self.test_doc, self.test_otherdoc)

    def testIter(self):
        self.db.save_docs(self.test_doc, self.test_otherdoc)
        for derp in self.db:
            pass

    def testAllDocs(self):
        self.db.all_docs()

    def testChanges(self):
        self.db.changes()
        self.db.changes(params={
            'feed': 'continuous'
        })

    def testViewCleanup(self):
        self.db.view_cleanup()

    def tearDown(self):
        self.db.delete()


class DocumentTest(ResourceTest):

    def setUp(self):
        super(DocumentTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))
        self.db.put()
        self.doc = self.db.document(self.doc_name)

    def testCrud(self):
        self.doc.put(params=self.test_doc)
        resp = self.doc.get()
        rev = resp.json()['_rev']
        self.doc.delete(rev)

    def testDict(self):
        self.db[self.doc_name] = self.test_doc
        self.db[self.doc_name]

    def testMerge(self):
        self.doc.put(params=self.test_doc)
        self.doc.merge(self.test_otherdoc)

    def testView(self):
        self.doc.view('_view', 'derp')

    def testAttachment(self):
        self.doc.attachment('file')

    def tearDown(self):
        self.db.delete()


class AttachmentTest(ResourceTest):
    pass


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
        for doc in [self.test_doc, self.test_otherdoc]:
            self.db.post(params=doc)
        for derp in self.db.all_docs():
            pass

    def tearDown(self):
        self.db.delete()


class ErrorTest(ResourceTest):

    def setUp(self):
        super(ErrorTest, self).setUp()
        self.db = divan.Database('/'.join([self.uri, self.db_name]))

    def testMissing(self):
        try:
            self.db.get()
            raise Exception("Shouldn't make it this far >:(")
        except LookupError:
            pass

if __name__ == "__main__":
    unittest.main()
