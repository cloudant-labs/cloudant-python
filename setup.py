#!/usr/bin/env python

from setuptools import setup
import os

setup(name='Divan',
      version='0.2.2',
      description='Asynchronous Cloudant / CouchDB Interface',
      author='Max Thayer',
      author_email='garbados@gmail.com',
      url='https://github.com/garbados/divan',
      packages=['divan'],
      install_requires=[
          'requests-futures==0.9.4',
      ],
      test_suite="test",
      # install with `pip install -e divan[doc]`
      extras_require={
      'docs': [
          'jinja2>=2.7',
          'markdown>=2.3.1'
      ]
      }
      )
