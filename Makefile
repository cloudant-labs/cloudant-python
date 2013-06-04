#!/bin/bash

# build src docs into a couchapp
default:
	python setup.py build

docs:
	python docs

clean:
	rm -rf dist build

install:
	python setup.py install

test:
	python setup.py test

.PHONY: docs