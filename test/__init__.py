import cloudant
from collections import defaultdict
import unittest


class ResourceTest(unittest.TestCase):

    def setUp(self):
        self.uri = 'http://localhost:5984'

        names = cloudant.Account(self.uri).uuids(4).json()['uuids']
        # database names must start with a letter
        names = ['a' + name for name in names]
        self.db_name = names[0]
        self.otherdb_name = names[1]
        self.doc_name = names[2]
        self.otherdoc_name = names[3]

        self.test_doc = {
            'herp': 'derp',
            'name': 'Luke Skywalker'
        }
        self.test_otherdoc = {
            'derp': 'herp',
            'name': 'Larry, the Incorrigible Miscreant'
        }

class AsyncTest(ResourceTest):

    def setUp(self):
        super(AsyncTest, self).setUp()
        self.account = cloudant.Account(self.uri, async=True)
        self.database = self.account.database(self.db_name)
        self.document = self.database.document(self.doc_name)

    def testSync(self):
        account = cloudant.Account(async=False)
        database = account[self.db_name]
        database.put().raise_for_status()
        database.delete().raise_for_status()

    def testAccount(self):
        future = self.account.get()
        response = future.result()
        response.raise_for_status()

    def testDatabase(self):
        future = self.database.put()
        response = future.result()
        response.raise_for_status()
        del self.account[self.db_name]

    def testDocument(self):
        future = self.database.put()
        response = future.result()
        response.raise_for_status()
        self.database[self.doc_name] = self.test_doc
        future = self.document.merge(self.test_otherdoc)
        response = future.result()
        response.raise_for_status()
        del self.account[self.db_name]

    def testIndex(self):
        future = self.database.put()
        response = future.result()
        response.raise_for_status()

        future = self.database.bulk_docs(self.test_doc, self.test_otherdoc)
        response = future.result()
        response.raise_for_status()

        total = []
        for doc in self.database:
            total.append(doc)
        assert len(total) == 2

        del self.account[self.db_name]

class AccountTest(ResourceTest):

    def setUp(self):
        super(AccountTest, self).setUp()
        self.account = cloudant.Account(self.uri)

    def testCloudant(self):
        account = cloudant.Account('garbados')
        assert account.uri == "https://garbados.cloudant.com"

    def testAllDbs(self):
        assert self.account.all_dbs().status_code == 200

    def testSession(self):
        assert self.account.session().status_code == 200

    def testActiveTasks(self):
        assert self.account.active_tasks().status_code == 200

    def testSecurity(self):
        username = 'user'
        password = 'password'
        # try auth login when admin party is on
        assert self.account.login(username, password).status_code == 401
        # disable admin party
        path = '_config/admins/%s' % username
        assert self.account.put(path, data="\"%s\"" %
                             password).status_code == 200
        # login, logout
        assert self.account.login(username, password).status_code == 200
        assert self.account.logout().status_code == 200
        # re-enable admin party
        assert self.account.login(username, password).status_code == 200
        assert self.account.delete(path).status_code == 200

    def testReplicate(self):
        self.db = self.account.database(self.db_name)
        assert self.db.put().status_code == 201

        resp = self.account.replicate(
            self.db_name,
            self.otherdb_name,
            params=dict(create_target=True))
        assert resp.status_code == 200

        assert self.db.delete().status_code == 200
        del self.account[self.otherdb_name]

    def testCreateDb(self):
        self.account.database(self.db_name)
        self.account[self.db_name]

    def testUuids(self):
        assert self.account.uuids().status_code == 200


class DatabaseTest(ResourceTest):

    def setUp(self):
        super(DatabaseTest, self).setUp()

        db_name = '/'.join([self.uri, self.db_name])
        self.db = cloudant.Database(db_name)

        response = self.db.put()
        response.raise_for_status()

    def testHead(self):
        assert self.db.head().status_code == 200

    def testGet(self):
        assert self.db.get().status_code == 200

    def testBulk(self):
        assert self.db.bulk_docs(
            self.test_doc, self.test_otherdoc).status_code == 201

    def testIter(self):
        assert self.db.bulk_docs(
            self.test_doc, self.test_otherdoc).status_code == 201
        for derp in self.db:
            pass

    def testAllDocs(self):
        resp = self.db.all_docs().get()
        assert resp.status_code == 200

    def testAllDocsWithKeys(self):
        resp = self.db.all_docs().get(params={'keys':['hello', 'goodbye']})
        assert resp.status_code == 200

    def testChanges(self):
        assert self.db.changes().status_code == 200
        assert self.db.changes(params={
            'feed': 'continuous'
        }).status_code == 200

    def testViewCleanup(self):
        assert self.db.view_cleanup().status_code == 202

    def testRevs(self):
        # put some docs
        assert self.db.bulk_docs(
            self.test_doc, self.test_otherdoc).status_code == 201
        # get their revisions
        revs = defaultdict(list)
        for doc in self.db:
            revs[doc['id']].append(doc['value']['rev'])
        assert self.db.missing_revs(revs).status_code == 200
        assert self.db.revs_diff(revs).status_code == 200

    def tearDown(self):
        assert self.db.delete().status_code == 200


class DocumentTest(ResourceTest):

    def setUp(self):
        super(DocumentTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        assert self.db.put().status_code == 201
        self.doc = self.db.document(self.doc_name)

    def testCrud(self):
        assert self.doc.put(params=self.test_doc).status_code == 201
        resp = self.doc.get()
        assert resp.status_code == 200
        rev = resp.json()['_rev']
        assert self.doc.delete(rev).status_code == 200

    def testDict(self):
        self.db[self.doc_name] = self.test_doc
        self.db[self.doc_name]

    def testMerge(self):
        # test upsert
        assert self.doc.merge(self.test_doc).status_code == 201
        # test merge
        assert self.doc.merge(self.test_otherdoc).status_code == 201

    def testAttachment(self):
        self.doc.attachment('file')

    def testNoLoginLogout(self):
        assert not hasattr(self.doc, 'login')
        assert not hasattr(self.doc, 'logout')

    def tearDown(self):
        assert self.db.delete().status_code == 200


class DesignTest(ResourceTest):

    def setUp(self):
        super(DesignTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        assert self.db.put().status_code == 201
        self.doc = self.db.design('ddoc')
        assert self.doc.put(params=self.test_doc).status_code == 201

    def testView(self):
        self.doc.index('_view/derp')
        self.doc.view('derp')
        self.doc.search('derp')

    def testList(self):
        # todo: test on actual list and show functions
        assert self.doc.list('herp', 'derp').status_code == 404
        assert self.doc.show('herp', 'derp').status_code == 500

    def tearDown(self):
        assert self.db.delete().status_code == 200


class AttachmentTest(ResourceTest):
    pass


class IndexTest(ResourceTest):

    def setUp(self):
        super(IndexTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))
        assert self.db.put().status_code == 201
        self.doc = self.db.document(self.doc_name)

    def testPrimaryIndex(self):
        """
        Show that views can be used as iterators
        """
        for doc in [self.test_doc, self.test_otherdoc]:
            assert self.db.post(params=doc).status_code == 201

        docs = []
        for derp in self.db.all_docs():
            docs.append(derp['id'])

        for derp in self.db.all_docs().iter(params=dict(descending=True, reduce=False)):
            assert docs.pop() == derp['id']

    def testQueryParams(self):
        view = self.db.all_docs()
        response = view.get(params=dict(reduce=False))
        assert 'reduce=False' not in response.url

    def tearDown(self):
        assert self.db.delete().status_code == 200


class ErrorTest(ResourceTest):

    def setUp(self):
        super(ErrorTest, self).setUp()
        self.db = cloudant.Database('/'.join([self.uri, self.db_name]))

    def testMissing(self):
        response = self.db.get()
        assert response.status_code == 404

if __name__ == "__main__":
    unittest.main()
