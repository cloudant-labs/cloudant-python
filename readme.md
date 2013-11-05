# Cloudant.py [![Build Status](https://travis-ci.org/cloudant-labs/cloudant-python.png)](https://travis-ci.org/cloudant-labs/cloudant-python) [![Coverage Status](https://coveralls.io/repos/cloudant-labs/cloudant-python/badge.png)](https://coveralls.io/r/cloudant-labs/cloudant-python) [![PyPi version](https://pypip.in/v/cloudant/badge.png)](https://crate.io/packages/cloudant/) [![PyPi downloads](https://pypip.in/d/cloudant/badge.png)](https://crate.io/packages/cloudant/)

[wiki]: http://en.wikipedia.org/wiki/Cloudant.py_(furniture\)
[wiki_img]: http://upload.wikimedia.org/wikipedia/commons/e/ea/FrancisLevettLiotard.jpg

An effortless Cloudant / CouchDB interface for Python.

## Install

    pip install cloudant
    
## Usage

Cloudant.py is an asynchronous wrapper around Python [Requests](http://www.python-requests.org/en/latest/) for interacting with CouchDB or Cloudant instances. Check it out:

    import cloudant

    # create a connection object
    conn = cloudant.Connection()
    # create a database object
    db = conn.database('test')
    # now, create the database on the server
    future = db.put()
    response = future.result()
    print response.json()
    # {'ok': True}

### Philosophy

Cloudant and CouchDB expose REST APIs that map effortlessly into native Python objects. As much as possible, Cloudant.py uses native Python objects as shortcuts to the raw API, so that such convenience never obscures what's going on underneath. For example:

    import cloudant

    conn = cloudant.Connection()
    db = conn.database('test')
    same_db = conn['test']
    assert db.uri == same_db.uri
    # True

Cloudant.py expose raw interactions -- HTTP requests, etc. -- through special methods, so we provide syntactical sugar without obscuring the underlying API. Built-ins, such as `__getitem__`, act as Pythonic shortcuts to those methods. For example:

    import cloudant

    conn = cloudant.Connection()
    db = conn.database('test')
    doc = db.document('test_doc')
    # create the document
    resp = doc.put({
      '_id': 'hello_world',
      'herp': 'derp'
      }).result()
    # delete the document
    rev = resp.json()['_rev']
    doc.delete(rev).result()
    # but this also creates a document
    db['hello_world'] = {'herp': 'derp'}

If CouchDB has a special endpoint for something, it's in Cloudant.py as a special method, so any special circumstances are taken care of automagically. For example:

    import cloudant

    conn = cloudant.Connection()
    db = conn.database('test')
    view = db.all_docs() # returns all docs in the database
    for doc in db:
      # iterates over every doc in the database
      pass
    for doc in view:
      # and so does this!
      pass

### Asynchronous

HTTP request methods like `get` and `post` return `Future` objects, which represent an eventual response. This allows your code to keep executing while the request is off doing its business in cyberspace. To wait for the response, use the `result` method, like so:

    import cloudant

    conn = cloudant.Connection()
    db = conn['test']
    future = db.put()
    response = future.result()
    print db.get().result().json()
    # {'db_name': 'test', ...}

As a result, any methods which must make an HTTP request return a `Future`.

### Option Inheritance

If you use one object to create another, the child will inherit the parents' settings. So, you can create a `Database` object explicitly, or use `Connection.database` to inherit cookies and other settings from the `Connection` object. For example:

    import cloudant

    conn = cloudant.Connection()
    db = conn.database('test')
    doc = db.document('test_doc')
    otherdoc = cloudant.Document('http://localhost:5984/test/test_doc')
    assert doc.uri == otherdoc.uri
    # True

## API
- [Connection](#Connection)
    - [Connection.active_tasks](#Connection.active_tasks)
    - [Connection.all_dbs](#Connection.all_dbs)
    - [Connection.database](#Connection.database)
    - [Connection.delete](#Connection.delete)
    - [Connection.get](#Connection.get)
    - [Connection.login](#Connection.login)
    - [Connection.logout](#Connection.logout)
    - [Connection.post](#Connection.post)
    - [Connection.put](#Connection.put)
    - [Connection.replicate](#Connection.replicate)
    - [Connection.session](#Connection.session)
    - [Connection.uuids](#Connection.uuids)
- [Database](#Database)
    - [Database.all_docs](#Database.all_docs)
    - [Database.changes](#Database.changes)
    - [Database.delete](#Database.delete)
    - [Database.design](#Database.design)
    - [Database.document](#Database.document)
    - [Database.get](#Database.get)
    - [Database.missing_revs](#Database.missing_revs)
    - [Database.post](#Database.post)
    - [Database.put](#Database.put)
    - [Database.revs_diff](#Database.revs_diff)
    - [Database.save_docs](#Database.save_docs)
    - [Database.view_cleanup](#Database.view_cleanup)
- [Document](#Document)
    - [Document.attachment](#Document.attachment)
    - [Document.delete](#Document.delete)
    - [Document.get](#Document.get)
    - [Document.merge](#Document.merge)
    - [Document.post](#Document.post)
    - [Document.put](#Document.put)
- [Design](#Design)
    - [Design.attachment](#Design.attachment)
    - [Design.delete](#Design.delete)
    - [Design.get](#Design.get)
    - [Design.index](#Design.index)
    - [Design.list](#Design.list)
    - [Design.merge](#Design.merge)
    - [Design.post](#Design.post)
    - [Design.put](#Design.put)
    - [Design.search](#Design.search)
    - [Design.show](#Design.show)
    - [Design.view](#Design.view)
- [View](#View)
    - [View.delete](#View.delete)
    - [View.get](#View.get)
    - [View.post](#View.post)
    - [View.put](#View.put)
- [Attachment](#Attachment)
    - [Attachment.delete](#Attachment.delete)
    - [Attachment.get](#Attachment.get)
    - [Attachment.post](#Attachment.post)
    - [Attachment.put](#Attachment.put)

<a name="Connection"></a>
### Connection(uri, **kwargs)

A connection to a Cloudant or CouchDB instance.

    connection = cloudant.Connection()
    connection.login(USERNAME, PASSWORD).result()
    print connection.get().result().json()
    # {"couchdb": "Welcome", ...}

<a name="Connection.active_tasks"></a>
#### Connection.active_tasks(**kwargs)

List replication, compaction, and indexer tasks currently running.

<a name="Connection.all_dbs"></a>
#### Connection.all_dbs(**kwargs)

List all databases.

<a name="Connection.database"></a>
#### Connection.database(name, **kwargs)

Create a `Database` object prefixed with this connection's URL.

<a name="Connection.delete"></a>
#### Connection.delete(path, **kwargs)

Make a DELETE request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Connection.get"></a>
#### Connection.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Connection.login"></a>
#### Connection.login(username, password, **kwargs)

Authenticate the connection via cookie.

<a name="Connection.logout"></a>
#### Connection.logout(**kwargs)

De-authenticate the connection's cookie.

<a name="Connection.post"></a>
#### Connection.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Connection.put"></a>
#### Connection.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Connection.replicate"></a>
#### Connection.replicate(source, target, opts, **kwargs)

Begin a replication job.
`opts` contains replication options such as whether the replication
should create the target (`create_target`) or whether the replication
is continuous (`continuous`).

Note: unless continuous, will not return until the job is finished.

<a name="Connection.session"></a>
#### Connection.session(**kwargs)

Get current user's authentication and authorization status.

<a name="Connection.uuids"></a>
#### Connection.uuids(count, **kwargs)

Generate an arbitrary number of UUIDs.

<a name="Database"></a>
### Database(uri, **kwargs)

Connection to a specific database.

Learn more about the raw API from the [Cloudant docs](http://docs.cloudant.com/api/database.html).

<a name="Database.all_docs"></a>
#### Database.all_docs(**kwargs)

Return a `View` object referencing all documents in the database.
You can treat it like an iterator:

    for doc in db.all_docs():
        print doc

<a name="Database.changes"></a>
#### Database.changes(**kwargs)

Gets a list of the changes made to the database.
This can be used to monitor for update and modifications to the database
for post processing or synchronization.

Automatically adjusts the request to handle the different response behavior
of polling, longpolling, and continuous modes.

For more information about the `_changes` feed, see
[the docs](http://docs.cloudant.com/api/database.html#obtaining-a-list-of-changes).

<a name="Database.delete"></a>
#### Database.delete(path, **kwargs)

Make a DELETE request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Database.design"></a>
#### Database.design(name, **kwargs)

Create a `Design` object from `name`, like so:

    db.design('test')
    # refers to DB/_design/test

<a name="Database.document"></a>
#### Database.document(name, **kwargs)

Create a `Document` object from `name`.

<a name="Database.get"></a>
#### Database.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Database.missing_revs"></a>
#### Database.missing_revs(revs, **kwargs)

Refers to [this method](http://docs.cloudant.com/api/database.html#retrieving-missing-revisions).

<a name="Database.post"></a>
#### Database.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Database.put"></a>
#### Database.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Database.revs_diff"></a>
#### Database.revs_diff(revs, **kwargs)

Refers to [this method](http://docs.cloudant.com/api/database.html#retrieving-differences-between-revisions)

<a name="Database.save_docs"></a>
#### Database.save_docs(**kwargs)

Save many docs, all at once. Each `doc` argument must be a dict, like this:

        db.save_docs({...}, {...}, {...})
        # saves all documents in one HTTP request

<a name="Database.view_cleanup"></a>
#### Database.view_cleanup(**kwargs)

Cleans up the cached view output on disk for a given view. For example:

    print db.view_cleanup().result().json()
    # {'ok': True}

<a name="Document"></a>
### Document(uri, **kwargs)

Connection to a specific document.

Learn more about the raw API from the [Cloudant docs](http://docs.cloudant.com/api/documents.html)

<a name="Document.attachment"></a>
#### Document.attachment(name, **kwargs)

Create an `Attachment` object from `name` and the settings
for the current database.

<a name="Document.delete"></a>
#### Document.delete(rev, **kwargs)

Delete the given revision of the current document. For example:

    rev = doc.get().result().json()['_rev']
    doc.delete(rev)

<a name="Document.get"></a>
#### Document.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Document.merge"></a>
#### Document.merge(change, **kwargs)

Merge `change` into the document,
and then `PUT` the updated document back to the server.

<a name="Document.post"></a>
#### Document.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Document.put"></a>
#### Document.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Design"></a>
### Design(uri, **kwargs)

Connection to a design document, which stores custom indexes and other database functions.

Learn more about design documents from the [Cloudant docs](http://docs.cloudant.com/api/design.html)

<a name="Design.attachment"></a>
#### Design.attachment(name, **kwargs)

Create an `Attachment` object from `name` and the settings
for the current database.

<a name="Design.delete"></a>
#### Design.delete(rev, **kwargs)

Delete the given revision of the current document. For example:

    rev = doc.get().result().json()['_rev']
    doc.delete(rev)

<a name="Design.get"></a>
#### Design.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Design.index"></a>
#### Design.index(function, **kwargs)

Create a `View` object referencing the secondary index at `_view/{function}`. For example:

    view = doc.index('index-name')
    # refers to /DB/_design/DOC/_view/index-name

For more on secondary indices, see
[Querying a View](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)

<a name="Design.list"></a>
#### Design.list(function, index, **kwargs)

Make a GET request to the list function at `_list/{function}/{index}`. For example:

    future = doc.list('list-name', 'index-name')
    # refers to /DB/_design/DOC/_list/list-name/index-name

For more details on list functions, see
[Querying List Functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-list-functions).

<a name="Design.merge"></a>
#### Design.merge(change, **kwargs)

Merge `change` into the document,
and then `PUT` the updated document back to the server.

<a name="Design.post"></a>
#### Design.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Design.put"></a>
#### Design.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Design.search"></a>
#### Design.search(function, **kwargs)

Creates a `View` object referencing the search index at `_search/{function}`. For example:

    view = doc.search('index-name')
    # refers to /DB/_design/DOC/_search/search-name

For more details on search indexes, see
[Searching for documents using Lucene queries](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)

<a name="Design.show"></a>
#### Design.show(function, id, **kwargs)

Make a GET request to the show function at `_show/{function}/{id}`. For example:

    future = doc.show('show-name', 'document-id')
    # refers to /DB/_design/DOC/_show/show-name/document-id

For more details on show functions, see
[Querying Show Functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-show-functions).

<a name="Design.view"></a>
#### Design.view(path, **kwargs)

Create a `View` object referencing the function at `path`. For example:

    view = doc.view('_view/index-name')
    # refers to /DB/_design/DOC/_view/index-name

<a name="View"></a>
### View(uri, **kwargs)

Methods for design document indexes and special methods.
Different kinds of indexes / methods will behave differently, so here are helpful docs:

* [Lucene search indexes](http://docs.cloudant.com/api/search.html#searching-for-documents-using-lucene-queries)
* [Secondary indexes / "views"](http://docs.cloudant.com/api/design-documents-querying-views.html#querying-a-view)
* [List functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-list-functions)
* [Show functions](http://docs.cloudant.com/api/design-documents-shows-lists.html#querying-show-functions)

Then, you just use basic HTTP methods to perform queries, like this:

    view.get(params=QUERY_ARGUMENTS)

Remember, before you can query an index, you have to make sure it's in your database.
See [these docs](http://docs.cloudant.com/api/design-documents-get-put-delete-copy.html#creating-or-updating-a-design-document)
for how to do that.

<a name="View.delete"></a>
#### View.delete(path, **kwargs)

Make a DELETE request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="View.get"></a>
#### View.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="View.post"></a>
#### View.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="View.put"></a>
#### View.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Attachment"></a>
### Attachment(uri, **kwargs)

Attachment methods for a single document

<a name="Attachment.delete"></a>
#### Attachment.delete(path, **kwargs)

Make a DELETE request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Attachment.get"></a>
#### Attachment.get(path, **kwargs)

Make a GET request against the object's URI joined
with `path`. `kwargs` are passed directly to Requests.

<a name="Attachment.post"></a>
#### Attachment.post(path, **kwargs)

Make a POST request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.

<a name="Attachment.put"></a>
#### Attachment.put(path, **kwargs)

Make a PUT request against the object's URI joined
with `path`.

`kwargs['params']` are turned into JSON before being
passed to Requests. If you want to indicate the message
body without it being modified, use `kwargs['data']`.


## Testing

To run Cloudant.py's tests, just do:

    python setup.py test

## Documentation

The API reference is automatically generated from the docstrings of each class and its methods. To install Cloudant.py with the necessary extensions to build the docs, do this:

    pip install -e cloudant[docs]

Then, in Cloudant.py's root directory, do this:
  
    python docs

Note: docstrings are in [Markdown](http://daringfireball.net/projects/markdown/).

## License

[MIT](http://opensource.org/licenses/MIT), yo.