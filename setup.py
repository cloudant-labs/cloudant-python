#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt', 'r') as f:
  dependencies = [line.strip() for line in f.readlines()]

setup(name='Divan',
      version='0.0.3',
      description='Effortless CouchDB ODM',
      author='Max Thayer',
      author_email='garbados@gmail.com',
      url='https://github.com/garbados/divan',
      packages=['divan'],
      install_requires=dependencies,
      test_suite="test",
      # install with `pip install -e divan[doc]`
      extras_require = {
            'docs': [
                  'jinja2>=2.7',
                  'markdown>=2.3.1'
            ]
      }
)
