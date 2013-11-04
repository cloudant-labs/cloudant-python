from requests_futures.sessions import FuturesSession
import json
import copy


class Resource(object):

    """
    REST resource class: implements GET, POST, PUT, DELETE methods
    for all other Divan objects, and manages settings inheritance.

    If you create an object, like a `Connection`, then use that to
    create a `Database` object, the `Database` will inherit any options
    from the `Connection` object, like

    Implements CRUD operations for all other Divan objects.
    """
    def __init__(self, uri, **kwargs):
        self.uri = uri

        if 'session' in kwargs.keys():
            self._session = kwargs['session']
            del kwargs['session']
        else:
            self._session = FuturesSession()

        self._set_options(**kwargs)

    def _set_options(self, **kwargs):
        if not hasattr(self, 'opts'):
            self.opts = {
                'headers': {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        if kwargs:
            self.opts.update(kwargs)

    def _make_url(self, path=''):
        """Joins the uri, and optional path"""
        if path:
            return '/'.join([self.uri, path])
        else:
            return self.uri

    def _validate(self, session, response):
        validate(response)

    def _make_request(self, method, path='', **kwargs):
        # kwargs supercede self.opts
        opts = copy.copy(self.opts)
        opts.update(kwargs)
        # normalize `params` kwarg according to method
        if method in ['post', 'put']:
            if 'params' in opts:
                opts['data'] = json.dumps(opts['params'])
                del kwargs['params']
        future = getattr(
            self._session,
            method)(
                self._make_url(
                    path),
                **opts)
        return future

    def get(self, path='', **kwargs):
        """
        Make a GET request against the object's URI joined
        with `path`. `kwargs` are passed directly to Requests.
        """
        return self._make_request('get', path, **kwargs)

    def put(self, path='', **kwargs):
        """
        Make a PUT request against the object's URI joined
        with `path`.

        `kwargs['params']` are turned into JSON before being
        passed to Requests. If you want to indicate the message
        body without it being modified, use `kwargs['data']`.
        """
        return self._make_request('put', path, **kwargs)

    def post(self, path='', **kwargs):
        """
        Make a POST request against the object's URI joined
        with `path`.

        `kwargs['params']` are turned into JSON before being
        passed to Requests. If you want to indicate the message
        body without it being modified, use `kwargs['data']`.
        """
        return self._make_request('post', path, **kwargs)

    def delete(self, path='', **kwargs):
        """
        Make a DELETE request against the object's URI joined
        with `path`. `kwargs` are passed directly to Requests.
        """
        return self._make_request('delete', path, **kwargs)
