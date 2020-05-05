#!/usr/bin/env python
# coding: utf-8

import functools
import json
import os
import requests
import sys
import urllib.parse
from typing import Callable
from typing import Any

CONSUMER_KEY_NAME = 'POCKET_CONSUMER_KEY'
ACCESS_TOKEN_NAME = 'POCKET_ACCESS_TOKEN'


def get_env_name(name: str) -> str:
    """Get environment value

    >>> import os
    >>> os.environ['A'] = 'B'
    >>> get_env_name('A')
    'B'

    Args:
        name (str): Environment name

    Returns:
        str: [TODO:description]
    """
    value = os.environ.get(name)
    if value is None:
        print("ERROR: %s is not set" % (name), file=sys.stderr)
        sys.exit(1)
    return value


def get_consumer_key() -> str:
    """Get Pocket consumer key"""
    return get_env_name(CONSUMER_KEY_NAME)


def get_access_token() -> str:
    """Get access token

    >>> import os
    >>> os.environ[ACCESS_TOKEN_NAME] = 'token'
    >>> get_access_token()
    'token'

    Returns:
        str: Access token
    """
    return get_env_name(ACCESS_TOKEN_NAME)


def get_method_arg_names(method: Callable[..., Any]) -> list:
    """Get the list of method arguments

    For example, given the method f(x, y), it returns [x , y].

    Args:
        method (Callable]): Methods to get arguments

    Returns:
        list: arguments
    """
    return list(method.__code__.co_varnames[:method.__code__.co_argcount])


def get_camel_from_snake(snake: str) -> str:
    """Get a camel format string from a snake format string

    >>> get_camel_from_snake('foo_bar_baz')
    'fooBarBaz'

    Args:
        snake (str): Snake style string

    Returns:
        str: Camel style string
    """
    return ''.join(map(
        lambda t: t[1].capitalize() if t[0] > 0 else t[1],
        enumerate(snake.split('_'))
    ))


def pocket_api_method(method: Callable[..., Any]) -> Callable:
    """A decorator to create and request for the Pocket API method"""

    @functools.wraps(method)
    def make_dic_and_request(self, *args, **kwargs):
        argnames = get_method_arg_names(method)
        argnames.remove('self')
        kwargs.update(dict(zip(argnames, args)))
        payload = dict()
        for k, v in kwargs.items():
            if v is not None:
                payload.update({get_camel_from_snake(k): v})
        return self._post(method.__name__, payload)

    return make_dic_and_request


class PocketClientException(Exception):
    pass


class PocketClient(object):
    def __init__(self, consumer_key: str, access_token: str):
        """Get PocketClient instance

        Args:
            consumer_key (str): Consumer key
            access_token (str): Access token
        """
        self._consumer_key = consumer_key
        self._access_key = access_token

    def _get_endpoint_url(self, api_method: str) -> str:
        """Get Pocket API endpoint url

        >>> p = PocketClient(None, None)
        >>> p._get_endpoint_url('retrieve')
        'https://getpocket.com/v3/get'
        >>> p._get_endpoint_url('add')
        'https://getpocket.com/v3/add'
        >>> p._get_endpoint_url('not-defined')
        Traceback (most recent call last):
            ...
        PocketClientException

        Args:
            api_method (str): [TODO:description]

        Returns:
            str: [TODO:description]
        """
        V3_API_ENDPOINT = "https://getpocket.com/v3/"
        API_METHOD_TO_PATH = {
                "retrieve": "get",
                "add": "add",
                }
        path = API_METHOD_TO_PATH.get(api_method)
        if path is None:
            raise PocketClientException()
        return urllib.parse.urljoin(V3_API_ENDPOINT, path)

    def _post(self, api_method: str, payload: dict) -> str:
        """Request POST method to an API endpoint

        Args:
            api_method (str): 'retrieve' or 'add'
            payload (dict): Payload to request

        Returns:
            str: JSON text
        """
        url = self._get_endpoint_url(api_method)
        headers = {'Content-Type': 'application/json'}
        payload.update(
                consumer_key=self._consumer_key,
                access_token=self._access_key)
        resp = requests.post(url, data=json.dumps(payload), headers=headers)
        if resp.status_code != 200:
            msg = resp.headers.get('X-Error')
            raise PocketClientException(msg)
        data = resp.json()
        return json.dumps(data)

    @pocket_api_method
    def retrieve(
            self, state: str = None, favorite: int = None, tag: str = None,
            content_type: str = None, detail_type: str = None,
            search: str = None, domain: str = None, since: int = None,
            count: int = None) -> str:
        """v3 API: Retrieve"""
        pass

    @pocket_api_method
    def add(
            self, url: str = None, title: str = None, tags: str = None,
            tweet_id: str = None) -> str:
        """v3 API: Add"""
        pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
