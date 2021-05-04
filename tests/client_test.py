import os
import unittest
from brandalert import Client
from datetime import date, timedelta
from brandalert import ParameterError, ApiAuthError


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """
    def setUp(self) -> None:
        self.client = Client(os.getenv('API_KEY'))

    def test_get_correct_data(self):
        response = self.client.preview(['test'])
        self.assertIsNotNone(response.domains_count)

    def test_extra_parameters(self):
        today = date.today()
        delta = timedelta(days=2)
        response = self.client.preview(
            ['test'],
            exlude_terms=['blog'],
            since_date=today - delta,
            with_typos=True,
            punycode=False
        )
        self.assertIsNotNone(response.domains_count)

    def test_empty_terms(self):
        with self.assertRaises(ParameterError):
            self.client.preview([])

    def test_incorrect_since_date(self):
        today = date.today()
        delta = timedelta(days=15)
        with self.assertRaises(ParameterError):
            self.client.preview(
                ['test'],
                since_date=today - delta
            )
        with self.assertRaises(ParameterError):
            self.client.preview(
                ['test'],
                since_date='incorrect value'
            )
        with self.assertRaises(ParameterError):
            self.client.preview(
                ['test'],
                since_date=None
            )

    def test_incorrect_with_typos(self):
        with self.assertRaises(ParameterError):
            self.client.preview(['test'], with_typos=None)
        with self.assertRaises(ParameterError):
            self.client.preview(['test'], with_typos='True')

    def test_incorrect_punycode(self):
        with self.assertRaises(ParameterError):
            self.client.preview(['test'], punycode=None)
        with self.assertRaises(ParameterError):
            self.client.preview(['test'], punycode='True')

    def test_incorrect_api_key(self):
        client = Client('at_00000000000000000000000000000')
        with self.assertRaises(ApiAuthError):
            client.preview(['test'])

    def test_raw_data(self):
        response = self.client.raw_data(
            ['test'],
            response_format=Client.XML_FORMAT,
            mode=Client.PREVIEW_MODE)
        self.assertTrue(response.startswith('<?xml'))


if __name__ == '__main__':
    unittest.main()
