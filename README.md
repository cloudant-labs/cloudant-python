# Divan [![Build Status](https://travis-ci.org/garbados/divan.png)](https://travis-ci.org/garbados/divan) [![Coverage Status](https://coveralls.io/repos/garbados/divan/badge.png)](https://coveralls.io/r/garbados/divan)

An effortless CouchDB ODM for Python.

Put on your favorite hookah, sit back on the [divan](http://en.wikipedia.org/wiki/Divan_(furniture\)), and relax.

<img src="http://upload.wikimedia.org/wikipedia/commons/e/ea/FrancisLevettLiotard.jpg"></img>

## Install

    pip install divan
    
## Usage

First up, connect to your database:

    import divan

    conn = divan.Connection()
    print conn.get('_all_dbs') # returns a list of your databases

Boom. Or:

    conn = divan.Connection("https://[username]:[password]@[uri]")
    print conn.put('divan') # creates a new database called 'divan'

### REST

Every object has methods like `get`, `post`, `put`, and `delete`, which correspond to CouchDB's REST API. In general, they work like this:

* get: Read an existing document
* post: Create a new document
* put: Update an existing document
* delete: Delete an existing document

These methods return HTTP responses, a la [requests](http://docs.python-requests.org/en/latest/). Call `json()` on the response to get the json body inside.

### Databases

You can create databases from a connection...

    import divan

    conn = divan.Connection('https://...')
    db = conn.database('divan')

...or from scratch:

    import divan

    db = divan.Database('https://...', 'divan')

#### Database.getOrCreate(docname='', **kwargs)

Gets or creates a document or the current database, like so:

    db = divan.Database('https://...', 'divan')
    # creates 'divan' database
    response = db.get_or_create()
    # creates 'sofamatic' documents
    response = db.get_or_create('sofamatic', params={...}) 

### Documents

Interact with documents through the `Database` object, like this:

    db = divan.Database('https://...', 'divan')
    response = db.get('sofamatic')
    doc = response.json()

#### Database.merge(docname, change, **kwargs):

Gets a document and updates it with your changes, like so:

    response = db.merge('sofamatic', {'comfy': True})

### Views

TODO implementation, tests, docs

### Attachments

TODO implementation, tests, docs

### Replications

TODO implementation, tests, docs

### Changes

TODO implementation, tests, docs

### Users

TODO implementation, tests, docs

### Security and Permissions

TODO implementation, tests, docs

## Testing

Testing uses a live database, so you'll need to configure a `local_settings.py` file or set environment variables for `URI`, `DB_NAME`, `USER`, and `PASS`. Then:

    python setup.py test