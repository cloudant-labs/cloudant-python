# Divan [![Build Status](https://travis-ci.org/garbados/divan.png)](https://travis-ci.org/garbados/divan) [![Coverage Status](https://coveralls.io/repos/garbados/divan/badge.png)](https://coveralls.io/r/garbados/divan)

An effortless CouchDB ODM for Python.

Put on your favorite hookah, sit back on the [divan][wiki], and relax.

![What a Divan Looks Like][wiki_img]

## Install

    pip install divan
    
## Usage
{% for class in order %}
{%- set main = docs[class]._main %}
### {{class}}({{main.args}}, {% if main.kwargs %}**{{main.kwargs}}{% endif %})
{{main.docs}}
{%- for name, method in docs[class].items() if name != '_main' %}
#### {{class}}.{{name}}({{method.args}}, {% if method.kwargs %}**{{method.kwargs}}{% endif %})
{{method.docs}}

{%- endfor %}
{%- endfor %}
## Testing

Testing uses a live database, so you'll need to configure a `local_settings.py` file or set environment variables for `URI`, `DB_NAME`, `USER`, and `PASS`. Then:

    python setup.py test

[wiki]: http://en.wikipedia.org/wiki/Divan_(furniture\)
[wiki_img]: http://upload.wikimedia.org/wikipedia/commons/e/ea/FrancisLevettLiotard.jpg