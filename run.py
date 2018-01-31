import smtplib
import sys

import os
import requests
import time
import json

from ses import send

account = sys.argv[1]
email_user = sys.argv[2]
data = {
    'action': 'account_history',
    'account': account,
    'count': 10,
}


def get_trans_history():
    host = os.getenv('RAIBLOCKS_HOST', '[::1]')
    return requests.post(f'http://{host}:7076', json.dumps(data)).json().get('history', [])


def notify(total, message):
    subject = 'Received {:10.5f} XRB'.format(total)
    if os.getenv('EMAIL_ENABLED', 'False') == 'True':
        send(email_user, subject, message)
    else:
        print(subject)
        print(message)


def check_account():
    trans_history = get_trans_history()
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
        notify(total, message)
    time.sleep(5)
    return trans_history


if __name__ == '__main__':
    last_known_trans = get_trans_history()
    while True:
        last_known_trans = check_account()
