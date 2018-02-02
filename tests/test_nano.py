import copy
import json
import unittest

import requests_mock

from app.nano import find_newest_trans


def match_count(count):
    return lambda r: str(count) in r.text


class TestNano(unittest.TestCase):

    @requests_mock.mock()
    def test_find_eleventh_new_transactions(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        ten_transactions['history'].pop(10)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), text=json.dumps(ten_transactions))
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(20), text=json.dumps(eleven_transactions))

        # When
        newest_transactions = find_newest_trans('nano_account', '11')

        assert newest_transactions == ten_transactions['history']
