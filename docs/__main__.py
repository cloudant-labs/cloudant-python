import inspect
import cloudant
import jinja2
import re
import os
from collections import OrderedDict

dirname, filename = os.path.split(os.path.abspath(__file__))
maindir = os.path.normpath(os.path.join(dirname, '..'))
docs = {}

def is_module(item):
    return inspect.ismodule(item)

def is_private(method_name):
    return bool(method_name[0] == "_")

def is_function(method):
    return hasattr(method, '__call__')

def get_first_indent(string):
    match = re.match(r'(\s{2,})\w', string)
    if match: 
        return match.groups()[0]
    else: 
        return match

def get_docs(method):
    try:
        arg_spec = get_args(method)
    except TypeError:
        arg_spec = get_args(method.__init__)
    docs = {
        'args': ', '.join(arg_spec.args[1:]),
        'kwargs': arg_spec.keywords
    }
    if method.__doc__:
        first_indent = get_first_indent(method.__doc__)
        if first_indent:
            docs['docs'] = method.__doc__.replace(first_indent, '\n')
        else:
            docs['docs'] = '\n' + method.__doc__ + '\n'
    return docs

def get_args(method):
    return inspect.getargspec(method)

for item_name in dir(cloudant):
    item = getattr(cloudant, item_name)
    if not (is_module(item) or is_private(item_name)):
        docs[item_name] = OrderedDict()
        docs[item_name]['_main'] = get_docs(item)
        if 'docs' not in docs[item_name]['_main'].keys():
            print "WARNING: %s.__init__ has no documentation!" % (item_name)
        for method_name in sorted(dir(item)):
            method = getattr(item, method_name)
            if is_function(method) and not is_private(method_name):
                if not method.__doc__:
                    print "WARNING: %s.%s has no documentation!" % (item_name, method_name)
                docs[item_name][method_name] = get_docs(method)

with open(os.path.join(dirname, 'readme_template.md'), 'r') as f:
    template = jinja2.Template(f.read())

with open(os.path.join(maindir,'readme.md'), 'w') as f:
    f.write(template.render(**{
        'docs': docs,
        'order': [
            'Connection', 
            'Database',
            'Document',
            'Design',
            'View',
            'Attachment'
        ]
    }))