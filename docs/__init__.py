import inspect
import divan
import jinja2
import re

docs = {}

def is_module(item):
  return inspect.ismodule(item)

def is_private(method_name):
  return bool(method_name[0] == "_")

def is_function(method):
  return hasattr(method, '__call__')

def get_first_indent(string):
  return re.match(r'(\s{2,})\w', string).groups()[0]

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
    docs['docs'] = method.__doc__.replace(first_indent, '\n')
  return docs

def get_args(method):
  return inspect.getargspec(method)

for item_name in dir(divan):
  item = getattr(divan, item_name)
  if not (is_module(item) or is_private(item_name)):
    docs[item_name] = {}
    docs[item_name]['_main'] = get_docs(item)
    for method_name in dir(item):
      method = getattr(item, method_name)
      if is_function(method) and not is_private(method_name):
        if not method.__doc__:
          print "WARNING: %s.%s has no documentation!" % (item_name, method_name)
        docs[item_name][method_name] = get_docs(method)

with open('reamde_template.md', 'r') as f:
  template = jinja2.Template(f.read())

with open('readme.md', 'w') as f:
  f.write(template.render(**{
    'docs': docs,
    'order': [
      'Connection', 
      'Database',
      'View',
      'Attachment'
    ]
  }))