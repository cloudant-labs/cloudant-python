import app
import unittest
import os

URI = os.environ['URI']
DB_NAME = os.environ['DB_NAME']
AUTH = (os.environ['USER'], os.environ['PASS'])

class ResourceTest(unittest.TestCase):
  def setUp(self):
    self.uri = URI
    self.db_name = DB_NAME
    self.auth = AUTH

class ConnectionTest(ResourceTest):
  def setUp(self):
    super(ConnectionTest, self).setUp()
    self.conn = app.Connection(self.uri, auth=self.auth)

class DatabaseTest(ResourceTest):
  def setUp(self):
    super(DatabaseTest, self).setUp()
    self.db = app.Database(self.uri, self.db_name, auth=self.auth)

  def testGet(self):
    assert self.db.get().json()['db_name'] == self.db_name

  def testPutAndDelete(self):
    """
    Create and delete a database
    """
    db = app.Database(self.uri, "testbutt", auth=self.auth)
    r = db.put()
    assert r.status_code == 201
    r = db.delete()
    assert r.status_code == 200

  def testDocs(self):
    ## POST
    animal = {'_id': 'soft vark', 'weight': 25}
    r = self.db.post(params=animal)
    if r.status_code == 201:
      animal['_rev'] = r.json()['rev']
    ## GET
    res = self.db.get(animal['_id']).json()
    if '_rev' not in animal:
      animal = res
    else:
      assert animal == res
    ## PUT
    animal['weight'] += 1
    r = self.db.put(animal['_id'], params=animal)
    animal['_rev'] = r.json()['rev']
    ## DELETE
    r = self.db.delete(animal['_id'], params={'rev': animal['_rev']})
    if 'ok' not in r.json():
      print r.json()
    assert r.json()['ok']

class AttachmentTest(ResourceTest):
  def setUp(self):
    super(AttachmentTest, self).setUp()
    self.attachment = app.Attachment(self.uri, self.db_name, 'hard vark', auth=self.auth)

  def testGet(self):
    print self.attachment.get().json()

class ViewTest(ResourceTest):
  def setUp(self):
    super(ViewTest, self).setUp()
    self.view = app.View(self.uri, self.db_name, 'derpview', auth=self.auth)

  def testGet(self):
    print self.view.get().json()

if __name__ == "__main__":
    unittest.main()