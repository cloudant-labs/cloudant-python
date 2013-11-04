#!/usr/bin/env python

from setuptools import setup

setup(name='Cloudant',
      version='0.2.0',
      description='Asynchronous Cloudant / CouchDB Interface',
      author='Max Thayer',
      author_email='garbados@gmail.com',
      url='https://github.com/cloudant-labs/cloudant',
      packages=['cloudant'],
      install_requires=[
          'requests-futures==0.9.4',
      ],
      test_suite="test",
      # install with `pip install -e cloudant[doc]`
      extras_require={
      'docs': [
          'jinja2>=2.7',
          'markdown>=2.3.1'
      ]
      }
      )
