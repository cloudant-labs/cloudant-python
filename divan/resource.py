import requests
import json
from .error import validate


class Resource(object):

    """
    REST resource class: implements GET, POST, PUT, DELETE methods
    and stores options to pass to requests
    """
    def __init__(self, uri, **kwargs):
        self.uri = uri
        self._set_options(**kwargs)

        for method in ['get', 'post', 'put', 'delete']:
            setattr(self, method, self._make_request(method))

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

    def _make_request(self, method, make_path=None):
        def inner(path='', **kwargs):
            kwargs.update(self.opts)
            # normalize `params` kwarg according to method
            if method in ['post', 'put']:
                if 'params' in kwargs:
                    kwargs['data'] = json.dumps(kwargs['params'])
                    del kwargs['params']
            # `make_path` changes `path` according to any special needs
            if make_path:
                path = make_path(path)
            response = getattr(
                requests,
                method)(
                    self._make_url(
                        path),
                    **kwargs)
            # handle errors
            validate(response)
            # handle cookies
            if response.cookies:
                self._set_options(cookies=response.cookies)
            return response
        return inner
