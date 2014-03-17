try:
    from requests_futures.sessions import FuturesSession
    requests_futures_available = True
except ImportError:
    requests_futures_available = False

import urlparse
import json
import copy

import requests


class RequestsFutureNotAvailable(Exception):
    message = "Please install request_sessions before proceeding."


class Resource(object):

    """
    REST resource class: implements GET, POST, PUT, DELETE methods
    for all other Divan objects, and manages settings inheritance.

    If you create an object, like an `Account`, then use that to
    create a `Database` object, the `Database` will inherit any options
    from the `Account` object, such as session cookies.

    Implements CRUD operations for all other Cloudant-Python objects.
    """
    def __init__(self, uri, **kwargs):
        self.uri = uri
        self.uri_parts = urlparse.urlparse(self.uri)

        if kwargs.get('session'):
            self._session = kwargs['session']
            del kwargs['session']
        elif kwargs.has_key('async'):
            if kwargs['async']:
                if not requests_futures_available:
                    raise RequestsFutureNotAvailable()
                self._session = FuturesSession()
            else:
                self._session = requests.Session()
            del kwargs['async']
        else:
            self._session = requests.Session()

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
            # if given a full URL, use that instead
            if urlparse.urlparse(path).scheme:
                return path
            else:
                return '/'.join([self.uri, path])
        else:
            return self.uri

    def _reset_path(self, path):
        parts = list(self.uri_parts)
        parts[2] = path
        url = urlparse.urlunparse(parts)
        return url

    def _make_request(self, method, path='', **kwargs):
        # kwargs supercede self.opts
        opts = copy.copy(self.opts)
        opts.update(kwargs)

        # normalize `params` kwarg according to method
        if 'params' in opts:
            if method in ['post', 'put']:
                opts['data'] = json.dumps(opts['params'])
                del opts['params']
            else:
                # cloudant breaks on True and False, so lowercase it
                params = opts['params']
                for key, value in params.items():
                    if value in [True, False]:
                        params[key] = str(value).lower()
                    elif type(value) in [list, dict, tuple]:
                        params[key] = json.dumps(value)
                opts['params'] = params

        # make the request
        future = getattr(
            self._session,
            method)(
                self._make_url(
                    path),
                **opts)
        return future

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
        return self.post(self._reset_path('_session'), headers=headers, data=data, **kwargs)

    def logout(self, **kwargs):
        """De-authenticate the connection's cookie."""
        return self.delete(self._reset_path('_session'), **kwargs)

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
