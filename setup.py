#!/usr/bin/env python

import os

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='cloudant',
      version='0.5.3',
      description='Asynchronous Cloudant / CouchDB Interface',
      author='Max Thayer',
      author_email='garbados@gmail.com',
      url='https://github.com/cloudant-labs/cloudant',
      packages=['cloudant'],
      license='MIT',
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
      },
      classifiers=[
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3'
      ],
      )
