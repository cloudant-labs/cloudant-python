cloudant
========

Python library to use the CloudAnt API

This library provides CRUD operations on Cloudant databases and documents.

**Example Usage**

	from cloudant.client import Client, Database
	
	client = Client('https://testing.cloudant.com, username='testing', password='testing')
	databases = client.get_all_databases()
	
	database = Database('test_db', client)
	
	docs = database.get_all_documents()
	
	doc = database.create_document(name='Route1', address={'street': '1923 South Street', 'city':'Omaha', 'state': 'NE'})
	
	database.delete_document(doc.id, doc.rev)
	
The goal is to eventually implement the entire Cloudant API.

The reference API version for this library is 1.0.2.

**Installation**

    pip install cloudant --use-mirrors

pypi seems to be acting funny, so `--use-mirrors` may be necessary.
