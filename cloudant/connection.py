from .resource import Resource
from .database import Database
import urlparse


class Connection(Resource):

    """
    A connection to a Cloudant or CouchDB instance.

        connection = cloudant.Connection()
        connection.login(USERNAME, PASSWORD).result()
        print connection.get().result().json()
        # {"couchdb": "Welcome", ...}
    """

    def __init__(self, uri="http://localhost:5984", **kwargs):
        if not urlparse.urlparse(uri).scheme:
            uri = "https://%s.cloudant.com" % uri
        super(Connection, self).__init__(uri, **kwargs)

    def database(self, name, **kwargs):
        """Create a `Database` object prefixed with this connection's URL."""
        opts = dict(self.opts.items() + kwargs.items())
        return Database(self._make_url(name), session=self._session, **opts)

    def __getitem__(self, name):
        """Shortcut to `Connection.database`."""
        return self.database(name, **self.opts)

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
