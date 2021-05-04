import unittest
from json import loads
from brandalert import Response, ErrorMessage


_json_response_ok = '''{
   "domainsCount": 2,
   "domainsList": [
        {
            "domainName": "blogginggoogle.com",
            "action": "added",
            "date": "2020-07-26"
        },
        {
            "domainName": "googleblog.asia",
            "action": "dropped",
            "date": "2020-07-26"
        }
    ]
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Response(response)
        self.assertEqual(parsed.domains_count, response['domainsCount'])
        self.assertIsInstance(parsed.domains_list, list)
        self.assertEqual(
            parsed.domains_list[0].domain_name,
            response['domainsList'][0]['domainName'])
        self.assertEqual(
            parsed.domains_list[0].action,
            response['domainsList'][0]['action'])
        self.assertEqual(
            str(parsed.domains_list[0].date),
            response['domainsList'][0]['date'])

        self.assertEqual(
            parsed.domains_list[1].domain_name,
            response['domainsList'][1]['domainName'])
        self.assertEqual(
            parsed.domains_list[1].action,
            response['domainsList'][1]['action'])
        self.assertEqual(
            str(parsed.domains_list[1].date),
            response['domainsList'][1]['date'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
