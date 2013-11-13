from .resource import Resource
from .database import Database
import urlparse


class Account(Resource):

    """
    A account to a Cloudant or CouchDB account.

        account = cloudant.Account()
        account.login(USERNAME, PASSWORD).result()
        print account.get().result().json()
        # {"couchdb": "Welcome", ...}
    """

    def __init__(self, uri="http://localhost:5984", **kwargs):
        if not urlparse.urlparse(uri).scheme:
            uri = "https://%s.cloudant.com" % uri
        super(Account, self).__init__(uri, **kwargs)

    def database(self, name, **kwargs):
        """Create a `Database` object prefixed with this account's URL."""
        opts = dict(self.opts.items() + kwargs.items())
        return Database(self._make_url(name), session=self._session, **opts)

    def __getitem__(self, name):
        """Shortcut to `Account.database`."""
        return self.database(name, **self.opts)

    def __delitem__(self, name):
        """
        Delete a database named `name`.
        Blocks until the response returns,
        and raises an error if the deletion failed.
        """
        return self.database(name, **self.opts).delete().result().raise_for_status()

    def all_dbs(self, **kwargs):
        """List all databases."""
        return self.get('_all_dbs', **kwargs)

    def active_tasks(self, **kwargs):
        """List replication, compaction, and indexer tasks currently running."""
        return self.get('_active_tasks', **kwargs)

    def replicate(self, source, target, opts={}, **kwargs):
        """
        Begin a replication job.
        `opts` contains replication options such as whether the replication
        should create the target (`create_target`) or whether the replication
        is continuous (`continuous`).

        Note: unless continuous, will not return until the job is finished.
        """

        params = {
            'source': source,
            'target': target
        }

        params.update(opts)
        if 'params' in kwargs:
            params.update(kwargs['params'])
            del kwargs['params']

        return self.post('_replicate', params=params, **kwargs)

    def uuids(self, count=1, **kwargs):
        """Generate an arbitrary number of UUIDs."""
        params = dict(count=count)
        return self.get('_uuids', params=params, **kwargs)
