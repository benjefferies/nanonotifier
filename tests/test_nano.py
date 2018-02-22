import copy
import json
import unittest
from unittest.mock import patch

import requests_mock
from requests import ConnectTimeout

from app.nano import find_newest_trans, check_account_for_new_pending, check_account_for_new_transactions


def match_count(count):
    return lambda request: json.loads(request.text)['count'] == count and json.loads(request.text)[
                                                                              'action'] == 'account_history'


def match_pending(request):
    return json.loads(request.text)['action'] == 'pending'


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

        # Then
        assert newest_transactions == ten_transactions['history']

    @requests_mock.mock()
    def test_find_new_transaction(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        last_known_transaction = ten_transactions['history'].pop(1)
        newest_transaction = ten_transactions['history'].pop(0)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), text=json.dumps(eleven_transactions))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            latest_transaction = check_account_for_new_transactions('nano_account', last_known_transaction['hash'],
                                                                    ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Received 0.00990 XRB from nano_account',
                                              AllStringsIn(['nano_account', '0.00990</a>XRB']),
                                              'received@nanotify.co')
        assert newest_transaction['hash'] == latest_transaction

    @requests_mock.mock()
    def test_find_new_transactions(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        last_known_transaction = ten_transactions['history'].pop(4)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), text=json.dumps(eleven_transactions))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            latest_transaction = check_account_for_new_transactions('nano_account', last_known_transaction['hash'],
                                                                    ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Received 0.06422 XRB from nano_account',
                                              AllStringsIn(['nano_account', '0.00990</a>XRB', '0.05432</a>XRB']),
                                              'received@nanotify.co')

        newest_transaction = ten_transactions['history'].pop(0)
        assert newest_transaction['hash'] == latest_transaction

    @requests_mock.mock()
    def test_keep_last_known_transaction_when_failed_to_get_second_page_of_history(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        ten_transactions['history'].pop(1)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), text=json.dumps(ten_transactions))
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(20), exc=ConnectTimeout)

        # When
        with patch('app.nano.send'), patch('app.nano.EMAIL_ENABLED', True):
            latest_transaction = check_account_for_new_transactions('nano_account', 'cant_get_to_this_id',
                                                                    ['test@example.com'])

        assert 'cant_get_to_this_id' == latest_transaction

    @requests_mock.mock()
    def test_dont_send_email_when_failed_to_get_second_page_of_history(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        ten_transactions['history'].pop(1)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10),
                          text=json.dumps(ten_transactions))
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(20), exc=ConnectTimeout)

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            check_account_for_new_transactions('nano_account', 'cant_get_to_this_id',
                                                                    ['test@example.com'])

            # Then
            mock_send.assert_not_called()

    @requests_mock.mock()
    def test_find_new_transactions_when_no_latest_known(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        newest_transaction = eleven_transactions['history'][0]
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), text=json.dumps(eleven_transactions))

        # When
        latest_transaction = check_account_for_new_transactions('nano_account', '', ['test@example.com'])

        # Then
        assert newest_transaction['hash'] == latest_transaction

    @requests_mock.mock()
    def test_find_new_transactions_when_raises_request_error_on_first(self, mock_request):
        # Given
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), exc=ConnectTimeout)

        # When
        latest_transaction = check_account_for_new_transactions('nano_account', '', ['test@example.com'])

        # Then
        assert latest_transaction is None

    @requests_mock.mock()
    def test_find_no_new_transactions_when_error_raised(self, mock_request):
        # Given
        with open('tests/11_transactions.json') as file:
            eleven_transactions = json.load(file)
        ten_transactions = copy.deepcopy(eleven_transactions)
        last_known_transaction = ten_transactions['history'].pop(1)
        mock_request.post('http://[::1]:7076', additional_matcher=match_count(10), exc=ConnectTimeout)

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            latest_transaction = check_account_for_new_transactions('nano_account', last_known_transaction['hash'],
                                                                    ['test@example.com'])

            # Then
            mock_send.assert_not_called()
        assert last_known_transaction['hash'] == latest_transaction



    @requests_mock.mock()
    def test_find_new_pending_transaction(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        new_pendings = copy.deepcopy(last_known_pending)
        new_pendings['blocks']['pending_2'] = {
            "amount": "20000000000000000000000000000000000",
            "source": "nano_account"
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, text=json.dumps(new_pendings))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', last_known_pending['blocks'],
                                                                ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Pending 20000.00000 XRB from nano_account',
                                              AllStringsIn(['nano_account', '20000.00000</a>XRB']),
                                              'pending@nanotify.co')
        assert newest_transactions == new_pendings['blocks']

    @requests_mock.mock()
    def test_find_new_pending_transactions(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        new_pendings = copy.deepcopy(last_known_pending)
        new_pendings['blocks']['pending_2'] = {
            "amount": "20000000000000000000000000000000000",
            "source": "nano_account"
        }
        new_pendings['blocks']['pending_3'] = {
            "amount": "30000000000000000000000000000000000",
            "source": "nano_account"
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, text=json.dumps(new_pendings))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', last_known_pending['blocks'],
                                                                ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Pending 50000.00000 XRB from nano_account',
                                              AllStringsIn(
                                                  ['nano_account', '20000.00000</a>XRB', '30000.00000</a>XRB']),
                                              'pending@nanotify.co')
        assert newest_transactions == new_pendings['blocks']

    @requests_mock.mock()
    def test_find_new_pending_transactions_no_prior_pending(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, text=json.dumps(last_known_pending))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', {}, ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Pending 10000.00000 XRB from nano_account',
                                              AllStringsIn(['nano_account', '10000.00000</a>XRB']),
                                              'pending@nanotify.co')

        # Then
        assert newest_transactions == last_known_pending['blocks']

    @requests_mock.mock()
    def test_find_new_pending_transactions_none_prior_pending(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, text=json.dumps(last_known_pending))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', {}, ['test@example.com'])

            # Then
            mock_send.assert_called_once_with('test@example.com', 'Pending 10000.00000 XRB from nano_account',
                                              AllStringsIn(['nano_account', '10000.00000</a>XRB']),
                                              'pending@nanotify.co')

        # Then
        assert newest_transactions == last_known_pending['blocks']

    @requests_mock.mock()
    def test_email_not_sent_when_none_pending(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, text=json.dumps(last_known_pending))

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', last_known_pending['blocks'],
                                                                ['test@example.com'])

            # Then
            mock_send.assert_not_called()
        assert newest_transactions == last_known_pending['blocks']

    @requests_mock.mock()
    def test_pending_email_not_sent_when_requests_fails(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, exc=ConnectTimeout)

        # When
        with patch('app.nano.send') as mock_send, patch('app.nano.EMAIL_ENABLED', True):
            check_account_for_new_pending('nano_account', last_known_pending['blocks'],
                                                                ['test@example.com'])

            # Then
            mock_send.assert_not_called()

    @requests_mock.mock()
    def test_pending_block_is_same_when_requests_fails(self, mock_request):
        # Given
        last_known_pending = {
            "blocks": {
                "pending_1": {
                    "amount": "10000000000000000000000000000000000",
                    "source": "nano_account"
                }
            }
        }
        mock_request.post('http://[::1]:7076', additional_matcher=match_pending, exc=ConnectTimeout)

        # When
        with patch('app.nano.send'), patch('app.nano.EMAIL_ENABLED', True):
            newest_transactions = check_account_for_new_pending('nano_account', last_known_pending['blocks'],
                                                                ['test@example.com'])

        assert newest_transactions == last_known_pending['blocks']


class AllStringsIn(list):
    def __eq__(self, email):
        return all(string in email for string in self)
