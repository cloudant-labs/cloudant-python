from .resource import Resource
from .database import Database


class Connection(Resource):

    def __init__(self, uri="http://localhost:5984", **kwargs):
        super(Connection, self).__init__(uri, **kwargs)

    def database(self, name, **kwargs):
        """Create a `Database` object prefixed with this connection's URL."""
        return Database(self._make_url(name), session=self._session, **kwargs)

    def __getitem__(self, name):
        """Shortcut to `Connection.database`."""
        return self.database(name)

    def info(self, **kwargs):
        """Return information about your CouchDB / Cloudant instance."""
        return self.get(**kwargs)

    def all_dbs(self, **kwargs):
        """List all databases."""
        return self.get('_all_dbs', **kwargs)

    def session(self, **kwargs):
        """Get current user's authentication and authorization status."""
        return self.get('_session', **kwargs)

    def login(self, username, password, **kwargs):
        """Authenticate the connection via cookie."""
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "name=%s&password=%s" % username, password
        return self.post('_session', headers=headers, data=data, **kwargs)

    def logout(self, **kwargs):
        """De-authenticate the connection's cookie."""
        return self.delete('_session', **kwargs)

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
