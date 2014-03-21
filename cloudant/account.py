from .resource import Resource
from .database import Database

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse


class Account(Resource):

    """
    An account to a Cloudant or CouchDB account.

        account = cloudant.Account()
        response = account.login(USERNAME, PASSWORD)
        print response.json()
        # { "ok": True, ... }

    Like all Cloudant-Python objects, pass `async=True`
    to make asynchronous requests, like this:

        account = cloudant.Account(async=True)
        future = account.login(USERNAME, PASSWORD)
        response = future.result()
        print response.json()
        # { "ok": True, ... }

    Although you can use `login` to request a cookie,
    you can also set `account._session.auth` to make Cloudant-Python
    use those credentials on every request, like this:

        account = cloudant.Account()
        account._session.auth = (username, password)
    """

    def __init__(self, uri="http://localhost:5984", **kwargs):
        if not urlparse.urlparse(uri).scheme:
            uri = "https://%s.cloudant.com" % uri
        super(Account, self).__init__(uri, **kwargs)

    def database(self, name, **kwargs):
        """Create a `Database` object prefixed with this account's URL."""
        opts = dict(self.opts, **kwargs)
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
        response = self.database(name, **self.opts).delete()
        # block until result if the object is using async
        if hasattr(response, 'result'):
            response = response.result()
        response.raise_for_status()

    def session(self, **kwargs):
        """Get current user's authentication and authorization status."""
        return self.get(self._reset_path('_session'), **kwargs)

    def login(self, username, password, **kwargs):
        """Authenticate the connection via cookie."""
        # set headers, body explicitly
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "name=%s&password=%s" % (username, password)
        return self.post(self._reset_path('_session'), headers=headers,
                         data=data, **kwargs)

    def logout(self, **kwargs):
        """De-authenticate the connection's cookie."""
        return self.delete(self._reset_path('_session'), **kwargs)

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
