import util
import os

ORDER = [
    'Account', 
    'Database',
    'Document',
    'Design',
    'Index',
    'Attachment'
]

dirname, filename = os.path.split(os.path.abspath(__file__))
maindir = os.path.normpath(os.path.join(dirname, '..'))

README = os.path.normpath(os.path.join(dirname, '..', 'readme.md'))
OUTPUT = os.path.join(dirname, 'site', 'index.html')
TEMPLATE = os.path.join(dirname, 'templates', 'index.html')

util.generate_docs(ORDER, TEMPLATE, OUTPUT, README)