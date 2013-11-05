import cloudant
from collections import defaultdict
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
        self.conn = cloudant.Connection(self.uri)

    def testAllDbs(self):
        assert self.conn.all_dbs().result().status_code == 200

    def testSession(self):
        assert self.conn.session().result().status_code == 200

    def testActiveTasks(self):
        assert self.conn.active_tasks().result().status_code == 200

    def testSecurity(self):
        username = 'user'
        password = 'password'
        # try auth login when admin party is on
        assert self.conn.login(username, password).result().status_code == 401
        # disable admin party
        path = '_config/admins/%s' % username
        assert self.conn.put(path, data="\"%s\"" %
                             password).result().status_code == 200
        # login, logout
        assert self.conn.login(username, password).result().status_code == 200
        assert self.conn.logout().result().status_code == 200
        # re-enable admin party
        assert self.conn.login(username, password).result().status_code == 200
        assert self.conn.delete(path).result().status_code == 200

    def testReplicate(self):
        self.db = self.conn.database(self.db_name)
        assert self.db.put().result().status_code == 201

        params = dict(create_target=True)
        assert self.conn.replicate(
            self.db_name, self.otherdb_name, params=params).result().status_code == 200

        assert self.db.delete().result().status_code == 200
        assert self.conn.delete(self.otherdb_name).result().status_code == 200

    def testCreateDb(self):
        self.conn.database(self.db_name)
        self.conn[self.db_name]

    def testUuids(self):
        assert self.conn.uuids().result().status_code == 200


class DatabaseTest(ResourceTest):

    def setUp(self):
        super(DatabaseTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        status = self.db.put().result().status_code
        print status
        assert status == 201

    def testGet(self):
        assert self.db.get().result().status_code == 200

    def testBulk(self):
        assert self.db.save_docs(
            self.test_doc, self.test_otherdoc).result().status_code == 201

    def testIter(self):
        assert self.db.save_docs(
            self.test_doc, self.test_otherdoc).result().status_code == 201
        for derp in self.db:
            pass

    def testAllDocs(self):
        self.db.all_docs()

    def testChanges(self):
        assert self.db.changes().result().status_code == 200
        assert self.db.changes(params={
            'feed': 'continuous'
        }).result().status_code == 200

    def testViewCleanup(self):
        assert self.db.view_cleanup().result().status_code == 202

    def testRevs(self):
        # put some docs
        assert self.db.save_docs(
            self.test_doc, self.test_otherdoc).result().status_code == 201
        # get their revisions
        revs = defaultdict(list)
        for doc in self.db:
            revs[doc['id']].append(doc['value']['rev'])
        assert self.db.missing_revs(revs).result().status_code == 200
        assert self.db.revs_diff(revs).result().status_code == 200

    def tearDown(self):
        assert self.db.delete().result().status_code == 200


class DocumentTest(ResourceTest):

    def setUp(self):
        super(DocumentTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        assert self.db.put().result().status_code == 201
        self.doc = self.db.document(self.doc_name)

    def testCrud(self):
        assert self.doc.put(params=self.test_doc).result().status_code == 201
        resp = self.doc.get().result()
        assert resp.status_code == 200
        rev = resp.json()['_rev']
        assert self.doc.delete(rev).result().status_code == 200

    def testDict(self):
        self.db[self.doc_name] = self.test_doc
        self.db[self.doc_name]

    def testMerge(self):
        assert self.doc.put(params=self.test_doc).result().status_code == 201
        assert self.doc.merge(self.test_otherdoc).result().status_code == 201

    def testView(self):
        self.doc.view('_view/derp')
        self.doc.index('derp')
        self.doc.search('derp')

    def testList(self):
        assert self.doc.list('herp', 'derp').result().status_code == 404
        assert self.doc.show('herp', 'derp').result().status_code == 404

    def testAttachment(self):
        self.doc.attachment('file')

    def tearDown(self):
        assert self.db.delete().result().status_code == 200


class AttachmentTest(ResourceTest):
    pass


class ViewTest(ResourceTest):

    def setUp(self):
        super(ViewTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        assert self.db.put().result().status_code == 201
        self.doc = self.db.document(self.doc_name)

    def testPrimaryIndex(self):
        """
        Show that views can be used as iterators
        """
        for doc in [self.test_doc, self.test_otherdoc]:
            assert self.db.post(params=doc).result().status_code == 201
        for derp in self.db.all_docs():
            pass

    def tearDown(self):
        assert self.db.delete().result().status_code == 200


class ErrorTest(ResourceTest):

    def setUp(self):
        super(ErrorTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))

    def testMissing(self):
        response = self.db.get().result()
        assert response.status_code == 404

if __name__ == "__main__":
    unittest.main()
