# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

import mock

from addthis.api import Addthis, AddthisEndpoint
from addthis.exceptions import AddthisError, AddthisValidationError


class TestAddThis(unittest.TestCase):
    """Tests for the ``Addthis`` class."""
    def setUp(self):
        self.addthis = Addthis(userid="test_userid",
                               password="test_password",
                               pubid="test_pubid")

    def test_init(self):
        self.assertEqual(self.addthis.userid, "test_userid")
        self.assertEqual(self.addthis.password, "test_password")
        self.assertEqual(self.addthis.pubid, "test_pubid")

    @mock.patch("addthis.api.AddthisEndpoint")
    def test_addthis_endpoint_creation(self, mock_endpoint):
        """Test that AddthisEndpoint object is created on Addthis object call.
        """
        self.addthis.shares.day()
        mock_endpoint.assert_called_once()

    def test_addthis_incorrect_num_of_parameters(self):
        self.assertRaises(AddthisValidationError,
                          lambda: self.addthis.one_param())


class TestAddthisEndpoint(unittest.TestCase):
    """Tests for the ``AddthisEndpoint`` class."""
    def setUp(self):
        self.endpoint = AddthisEndpoint(userid="test_userid",
                                        password="test_password",
                                        pubid="",
                                        path=None)

    def test_api_version(self):
        self.assertEqual(self.endpoint.API_VERSION, 1.0)

    def test_api_base_url(self):
        self.assertEqual(self.endpoint.BASE_URL,
                         "https://api.addthis.com/analytics/1.0/pub/")

    def test_make_request_url_is_correct(self):
        url = self.endpoint._make_request_url("shares", "day")
        self.assertEqual(url,
                         "https://api.addthis.com/analytics/1.0/pub/shares/"
                         "day.json")

    def test_make_query_params_empty(self):
        """Tests that _make_query_params returns an empty dictionary when
        there is no query_parameters and pubid is not specified
        """
        params = self.endpoint._make_query_params(query_params=None)
        self.assertEqual(params, {})

    def test_make_query_params_non_empty(self):
        """Tests that _make_query_params correctly populates a dictionary
        with parameters.
        """
        params = self.endpoint._make_query_params(
            query_params={"pubid": "test_pubid", "key": "value"})
        self.assertEqual(params, {"pubid": "test_pubid", "key": "value"})

    def test_query_params_pubid_assignment(self):
        """Tests that _make_query_params correctly populates a dictionary
        with pubid from the AddthisEndpoint object.
        """
        self.endpoint.pubid = "test_pubid"
        params = self.endpoint._make_query_params(query_params=None)
        self.assertEqual(params, {"pubid": "test_pubid"})

    @mock.patch("addthis.api.AddthisEndpoint.request")
    def test_getattr(self, mock_request):
        """Tests that ``path`` dictionary is correctly populated on
        __getattr__ calls. """
        mock_request.return_value = []
        endpoint = self.endpoint
        response = endpoint.shares.day()
        self.assertEqual(endpoint.path, ["shares", "day"])
        self.assertEqual(response, [])

    @mock.patch("requests.get")
    def test_make_request(self, mock_requests_get):
        mock_requests_get.return_value = []
        self.endpoint._make_request("test_url", {"test_key": "test_value"})
        mock_requests_get.assert_called_with(
            "test_url", params={"test_key": "test_value"},
            auth=("test_userid", "test_password"))

    @mock.patch("addthis.api.AddthisEndpoint._make_request")
    @mock.patch("addthis.api.AddthisEndpoint._make_query_params")
    @mock.patch("addthis.api.AddthisEndpoint._make_request_url")
    def test_request(self, mock_make_request_url, mock_make_query_params,
                     mock_make_request):
        mock_make_request_url.return_value = "test_url"
        mock_make_query_params.return_value = {"test_key": "test_value"}
        mock_make_request.return_value.status_code = 200

        self.endpoint.request("shares", "day",
                              query_params={"test_key": "test_value"})

        mock_make_request_url.assert_called_with("shares", "day")
        mock_make_query_params.assert_called_with({"test_key": "test_value"})
        mock_make_request.assert_called_with("test_url",
                                             {"test_key": "test_value"})

    @mock.patch("addthis.api.AddthisEndpoint._make_request")
    @mock.patch("addthis.api.AddthisEndpoint._make_query_params")
    @mock.patch("addthis.api.AddthisEndpoint._make_request_url")
    def test_request_raising_exception(self, mock_make_request_url,
                                       mock_make_query_params,
                                       mock_make_request):
        """Uses mock response object with status code 400 and a message
        that indicates an API error.
        """
        mock_make_request.return_value.status_code = 400
        mock_make_request.return_value.json.return_value = {"error": {
            "message": "invalid parameter",
            "code": 30,
            "attachment": {"reason": ""}}
        }

        try:
            self.endpoint.request("shares", "day",
                                  query_params={"test_key": "test_value"})
        except AddthisError as e:
            self.assertEqual(e.status_code, 400)
            self.assertEqual(e.message, "invalid parameter")
            self.assertEqual(e.code, 30)
            self.assertEqual(e.attachment, {"reason": ""})

        except Exception as e:
            self.fail("Unexpected exception thrown: {!s}".format(e))
        else:
            self.fail("AddthisError not thrown")

    def test_addthis_request(self):
        """Executes the actual request to the AddThis API with incorrect
        credentials.
        """
        try:
            self.endpoint.request("shares", "day")
        except AddthisError as e:
            self.assertEqual(e.status_code, 401)
            self.assertEqual(e.message, "authentication failed")
            self.assertEqual(e.code, 80)
            self.assertEqual(e.attachment, {"nonce": None,
                                            "realm": "AddThis",
                                            "opaque": None})

        except Exception as e:
            self.fail("Unexpected exception thrown: {!s}".format(e))
        else:
            self.fail("AddthisError not thrown")