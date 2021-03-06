from decimal import Decimal

import mock
from requests import Response
from unittest2 import TestCase

from restorm.clients.jsonclient import JSONClient, JSONClientMixin


class JSONClientTests(TestCase):
    def setUp(self):
        self.client = JSONClient()

    @mock.patch('requests.request')
    def test_get(self, request):
        response = Response()
        response.status_code = 200
        response._content = '{"foo": "bar"}'
        response.headers['Content-Type'] = 'application/json'
        request.return_value = response

        response = self.client.get(uri='http://localhost/api')

        data = response.content
        self.assertIsInstance(data, dict)
        self.assertTrue('foo' in data)
        self.assertEqual(data['foo'], 'bar')

    @mock.patch('requests.request')
    def test_incorrect_content_type(self, request):
        response = Response()
        response.status_code = 200
        response._content = '{"foo": "bar"}'
        response.headers['Content-Type'] = 'foobar'
        request.return_value = response
        response = self.client.get(uri='http://localhost/api')

        data = response.content
        self.assertIsInstance(data, basestring)
        self.assertEqual(data, '{"foo": "bar"}')


class JSONClientMixinTests(TestCase):
    def setUp(self):
        self.mixin = JSONClientMixin()

    def test_empty(self):
        original_data = None

        serialized_data = self.mixin.serialize(original_data)
        self.assertEqual(serialized_data, '')

        deserialized_data = self.mixin.deserialize(serialized_data)
        self.assertEqual(original_data, deserialized_data)

    def test_empty_string(self):
        original_data = ''

        serialized_data = self.mixin.serialize(original_data)
        self.assertEqual(serialized_data, '""')

        deserialized_data = self.mixin.deserialize(serialized_data)
        self.assertEqual(original_data, deserialized_data)

    def test_complex_data(self):
        original_data = {'a': ['b', 'c', 1, Decimal('2.3')]}

        serialized_data = self.mixin.serialize(original_data)
        self.assertEqual(serialized_data, '{"a": ["b", "c", 1, 2.3]}')

        deserialized_data = self.mixin.deserialize(serialized_data)
        self.assertEqual(original_data, deserialized_data)
