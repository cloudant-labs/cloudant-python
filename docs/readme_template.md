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
{%- for class in order %}
- [{{class}}](#{{class}})
{%- for name in docs[class].keys() if name != '_main' %}
    - [{{class}}.{{name}}](#{{class}}.{{name}})
{%- endfor %}
{%- endfor %}
{% for class in order %}
{%- set main = docs[class]._main %}
<a name="{{class}}"></a>
### {{class}}({{main.args}}{% if main.args and main.kwargs%}, {% endif %}{% if main.kwargs %}**{{main.kwargs}}{% endif %})
{{main.docs}}
{%- for name, method in docs[class].items() if name != '_main' %}
<a name="{{class}}.{{name}}"></a>
#### {{class}}.{{name}}({{method.args}}{% if method.args and method.kwargs%}, {% endif %}{% if method.kwargs %}**{{method.kwargs}}{% endif %})
{{method.docs}}

{%- endfor %}
{%- endfor %}

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