# Divan [![Build Status](https://travis-ci.org/garbados/divan.png)](https://travis-ci.org/garbados/divan) [![Coverage Status](https://coveralls.io/repos/garbados/divan/badge.png)](https://coveralls.io/r/garbados/divan)

An effortless CouchDB ODM for Python.

Put on your favorite hookah, sit back on the [divan][wiki], and relax.

![What a Divan Looks Like][wiki_img]

## Install

    pip install divan
    
## Usage

### Connection(uri, **kwargs)

#### Connection.database(name, **kwargs)

### Database(uri, name, **kwargs)

Connection to a specific database

#### Database.bulk_docs(docs, )

#### Database.merge(docname, change, **kwargs)

Get document, merge changes, put updated document

#### Database.attachment(doc, **kwargs)

#### Database.get_or_create(docname, **kwargs)

Get; if nothing is found, post (doc) or put (db)

#### Database.view(doc, **kwargs)

### View(uri, name, doc, **kwargs)

Methods for design documents

#### View.query(viewname, **kwargs)

### Attachment(uri, name, doc, **kwargs)

Attachment methods for a single document

## Testing

Testing uses a live database, so you'll need to configure a `local_settings.py` file or set environment variables for `URI`, `DB_NAME`, `USER`, and `PASS`. Then:

    python setup.py test

[wiki]: http://en.wikipedia.org/wiki/Divan_(furniture\)
[wiki_img]: http://upload.wikimedia.org/wikipedia/commons/e/ea/FrancisLevettLiotard.jpg