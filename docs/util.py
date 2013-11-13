import inspect
import cloudant
import jinja2
import markdown
import re

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
    # get the source code
    source = inspect.getsource(method).replace(method.__doc__, '').replace('""""""', '')

    # get the docstring
    if method.__doc__:
        first_indent = get_first_indent(method.__doc__)
        if first_indent:
            docstring = method.__doc__.replace(first_indent, '\n')
        else:
            docstring = '\n' + method.__doc__ + '\n'
    else:
        docstring = ''

    # get arguments
    try:
        arg_spec = inspect.getargspec(method)
    except TypeError:
        arg_spec = inspect.getargspec(method.__init__)
    args = ', '.join(arg_spec.args[1:])
    kwargs = arg_spec.keywords
    
    # mush it together
    return {
        'args': ', '.join([args, kwargs]),
        'docs': docstring,
        'html': markdown.markdown(docstring),
        'code': source
    }

def get_sections(order):
    docs = []
    for item_name in order:
        item = getattr(cloudant, item_name)
        if not (is_module(item) or is_private(item_name)):
            section = dict(
                head = get_docs(item),
                name = item_name,
                methods = []
                )
            if not item.__doc__:
                print "WARNING: %s has no documentation!" % (item_name)
            for method_name in sorted(dir(item)):
                method = getattr(item, method_name)
                if is_function(method) and not is_private(method_name):
                    if not method.__doc__:
                        print "WARNING: %s.%s has no documentation!" % (item_name, method_name)
                    method_docs = get_docs(method)
                    method_docs['name'] = method_name
                    section['methods'].append(method_docs)
            docs.append(section)
    return docs

def generate_docs(order, template, output, readme):
    sections = get_sections(order)

    with open(template, 'r') as f:
        template = jinja2.Template(f.read())

    with open(readme, 'r') as f:
        readme = markdown.markdown(f.read(), ['fenced_code'])

    with open(output, 'w') as f:
        f.write(template.render(sections=sections, readme=readme))