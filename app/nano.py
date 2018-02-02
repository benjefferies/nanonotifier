import json
import logging
import os

import requests

from app.ses import send

logger = logging.getLogger(__name__)

data = {
    'action': 'account_history'
}
host = os.getenv('RAIBLOCKS_HOST', '[::1]')


def get_trans_history(account, count):
    req = dict(account=account, count=count, **data)
    return requests.post(f'http://{host}:7076', json.dumps(req)).json().get('history', [])


def notify(emails, total, message):
    subject = 'Received {:10.5f} XRB'.format(total)
    if os.getenv('EMAIL_ENABLED', 'False') == 'True':
        for email in emails:
            send(email, subject, message)
    else:
        logger.info(subject)
        logger.info(message)


def find_newest_trans(account, last_known_trans, count=10):
    trans_history = get_trans_history(account, count)
    new_trans = []
    for tran in trans_history:
        if tran['hash'] != last_known_trans:
            new_trans.append(tran)
        else:
            return new_trans
    # Recursively search until all newest_transactions found
    return find_newest_trans(account, last_known_trans, count=count+10)


def check_account(account, last_known_trans, emails):
    new_trans = []
    # Get last transaction if none
    if not last_known_trans:
        history = get_trans_history(account, 1)
        last_known_trans = history[0].get('hash') if history else None

    if last_known_trans:
        new_trans = find_newest_trans(account, last_known_trans)
    total = 0
    message = ''
    for tran in new_trans:
        if tran['type'] == 'receive':
            from_account = tran['account']
            amount = float(tran['amount'])
            if amount != 0:
                amount /= 1.0e+30
            total += amount
            message += f'New transaction from {from_account} for ' + "{:10.5f} XRB\n".format(amount)
    if total > 0:
        notify(emails, total, message)
    return last_known_trans if not new_trans else new_trans[0].get('hash')
