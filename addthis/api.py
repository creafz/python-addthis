# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import requests

from addthis.exceptions import AddthisError, AddthisValidationError


class Addthis(object):
    """Base class that keeps authentication parameters and instantiates
    an ``AddthisEndpoint`` object.
    """
    def __init__(self, userid, password, pubid=None):
        """ ``userid``

              Your AddThis userid or email address.

            ``password``

              Your AddThis password.

            ``pubid``

              The publisher profile for which you are requesting data. If
              you specify it in constructor it will be used in all requests.
              Alternatively you can pass it as a parameter for the each
              request.
        """

        self.userid = userid
        self.password = password
        self.pubid = pubid

    def __getattr__(self, path):
        """Returns a callable ``AddthisEndpoint`` object that will execute
        the query.
        """
        return AddthisEndpoint(self.userid, self.password, self.pubid, path)


class AddthisEndpoint(object):
    """Actual object that executes queries to the Addthis Analytics API."""
    API_VERSION = 1.0
    BASE_URL = "https://api.addthis.com/analytics/{api_version}/pub/"\
        .format(api_version=API_VERSION)

    def __init__(self, userid, password, pubid, path):
        self.userid = userid
        self.password = password
        self.pubid = pubid
        self.path = []

        if path:
            self.path.append(path)

    def __getattr__(self, path):
        self.path.append(path)
        return self

    def __call__(self, *args, **kwargs):
        """Checks that there are 2 parameters in the ``path`` list:
        the first one is ``metric`` and the second one is ``dimension``
        Raises an Exception if the number of parameters is different.
        """

        if len(self.path) != 2:
            raise AddthisValidationError("Incorrect number of parameters "
                                         "are given. Expected 2 but got "
                                         "{num_params}"
                                         .format(num_params=len(self.path)))
        metric = self.path[0]
        dimension = self.path[1]

        return self.request(metric, dimension, query_params=kwargs)

    def _make_request_url(self, metric, dimension):
        return "{0}{1}/{2}.json".format(self.BASE_URL, metric, dimension)

    def _make_query_params(self, query_params):
        if query_params is None:
            query_params = {}
        if "pubid" not in query_params and self.pubid:
            query_params["pubid"] = self.pubid
        return query_params

    def _make_request(self, url, query_params):
        return requests.get(url, params=query_params, auth=(self.userid,
                                                            self.password))

    def request(self, metric, dimension, query_params=None):
        """Given metric, dimension and query parameters constructs the url
        and executes the query. If response status code is not 200 raises an
        Exception populated with data returned from Addthis. Returns
        a dictionary with data if request was successful.
        """
        url = self._make_request_url(metric, dimension)
        query_params = self._make_query_params(query_params)
        response = self._make_request(url, query_params)

        data = response.json()
        if response.status_code != 200:
            raise AddthisError(response.status_code, data["error"])
        return data