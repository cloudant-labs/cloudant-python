# coding=utf-8

from cloudant.client import Client
from cloudant.database import Database

try:
    from local_credentials import URL, AUTH_KEY, AUTH_PASS
except:
    pass

def main():
    client = Client(URL, AUTH_KEY, AUTH_PASS)
    print(client.get_all_dbs())
    print(client.get_database_info('test'))
    print(client.create_database('octopus'))
    print(client.get_all_dbs())
    print(client.delete_database('octopus'))
    print(client.get_all_dbs())

    db = Database('crud', client=client)
    print(db.get_all_documents(descending=True))


if __name__ == '__main__':
    main()
