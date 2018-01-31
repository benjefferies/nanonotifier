import json
import os
import sys
import time

import requests

from app.ses import send

data = {
    'action': 'account_history',
    'count': 10,
}
host = os.getenv('RAIBLOCKS_HOST', '[::1]')


def get_trans_history(account):
    req = dict(account=account, **data)
    return requests.post(f'http://{host}:7076', json.dumps(req)).json().get('history', [])


def notify(emails, total, message):
    subject = 'Received {:10.5f} XRB'.format(total)
    if os.getenv('EMAIL_ENABLED', 'False') == 'True':
        for email in emails:
            send(email, subject, message)
    else:
        print(subject)
        print(message)


def check_account(account, last_known_trans, emails):
    trans_history = get_trans_history(account)
    new_trans = [x for x in trans_history if x not in last_known_trans]
    total = 0
    message = ''
    for tran in new_trans:
        if tran['type'] == 'receive':
            from_account = tran['account']
            amount = float(tran['amount'])
            if amount != 0:
                amount /= 1.0e+30
            total += amount
            message += f'New transaction from {from_account} for ' + "{:10.5f}\n".format(amount)
    if total > 0:
        notify(emails, total, message)
    time.sleep(5)
    return trans_history