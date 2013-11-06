import util
import os

ORDER = [
    'Connection', 
    'Database',
    'Document',
    'Design',
    'View',
    'Attachment'
]

dirname, filename = os.path.split(os.path.abspath(__file__))
maindir = os.path.normpath(os.path.join(dirname, '..'))

README = os.path.normpath(os.path.join(dirname, '..', 'readme.md'))
OUTPUT = os.path.join(dirname, 'dist', 'index.html')
TEMPLATE = os.path.join(dirname, 'templates', 'index.html')

util.generate_docs(ORDER, TEMPLATE, OUTPUT, README)