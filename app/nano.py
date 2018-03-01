import json
import logging
import os
from collections import defaultdict

import jinja2
import requests
from requests import RequestException

from app import ses, fcm
from app.config import HOST, EMAIL_ENABLED, WEBHOOK_ENABLED, WEBHOOK_TIMEOUT, FCM_ENABLED

logger = logging.getLogger(__name__)

history_data = {
    'action': 'account_history'
}
pending_data = {
    'action': 'pending',
    'source': 'true'
}


def get_trans_history(account, count):
    req = dict(account=account, count=count, **history_data)
    try:
        return requests.post(f'http://{HOST}:7076', json.dumps(req)).json().get('history', [])
    except RequestException as e:
        logger.exception('Failed to get transaction history: ', str(e))
        return []


def get_pendings(account, last_known_pendings=None):
    req = dict(account=account, **pending_data)
    try:
        pending = requests.post(f'http://{HOST}:7076', json.dumps(req)).json()
        return pending['blocks'] if pending.get('blocks') else {}
    except RequestException as e:
        logger.exception('Failed to get transaction history: ', str(e))
        return last_known_pendings or {}


def notify(emails, message, subject, from_email):
    if EMAIL_ENABLED:
        logger.debug(f'Sending emails to {str(emails)}')
        logger.debug(f'{subject}\n\n{message}')
        for email in emails:
            ses.send(email, subject, message, from_email)
    else:
        logger.info(subject)
        logger.info(message)


def webhook_notify(webhooks, subject, account, amount, transaction_type):
    if WEBHOOK_ENABLED:
        payload = {'account': account, 'amount': amount, 'type': transaction_type, 'text': subject}
        for webhook in webhooks:
            try:
                r = requests.post(webhook, data=json.dumps(payload), timeout=WEBHOOK_TIMEOUT)
                logger.debug(f'{webhook} returned status code {r.status_code}')
            except RequestException:
                logger.exception('Failed to trigger webhook')
            logger.debug(f'Sent http request to {webhook}')


def queue_notify(subject, account):
    if FCM_ENABLED:
        logger.debug(f'Sending sns message for {account}')
        fcm.send(account, subject)


def find_new_pending_trans(all_pending, last_known_pending):
    new_pending = {}
    for tran_hash in all_pending.keys():
        if not last_known_pending.get(tran_hash):
            new_pending[tran_hash] = all_pending[tran_hash]

    logger.debug(f'Found new pending transactions {json.dumps(new_pending, indent=4, sort_keys=True)}')
    return new_pending


def find_newest_trans(account, last_known_trans, count=10):
    trans_history = get_trans_history(account, count)
    if not trans_history:
        return trans_history
    new_trans = []
    for tran in trans_history:
        if tran['hash'] != last_known_trans:
            new_trans.append(tran)
        else:
            return new_trans
    # Recursively search until all newest_transactions found
    return find_newest_trans(account, last_known_trans, count=count+10)


def check_account_for_new_transactions(account, last_known_trans, emails, webhooks=None):
    logger.info(f'Finding new transactions for {account}')
    # Get last transaction if none
    if not last_known_trans:
        logger.debug(f'No known transactions for {account}')
        history = get_trans_history(account, 10)
        return history[0].get('hash') if history else None

    new_trans = find_newest_trans(account, last_known_trans)
    logger.debug(f'Found new transactions {json.dumps(new_trans, indent=4, sort_keys=True)}')
    message, total = build_message_and_total_for_new_transactions(account, new_trans)
    if total:
        subject = 'Received {total:1.5f} XRB at {account}'.format(total=total, account=account)
        notify(emails, message, subject, from_email='received@nanotify.co')
        webhook_notify(webhooks, subject, account, total, transaction_type='received')
        queue_notify(subject, account)
    return last_known_trans if not new_trans else new_trans[0].get('hash')


def check_account_for_new_pending(account, last_known_pendings, emails, webhooks=None):
    logger.info(f'Finding pending transactions for {account}')
    # Get last transaction if none
    pendings = get_pendings(account, last_known_pendings)
    if any(last_known_pendings):
        logger.debug(f'No known pending transactions for {account}')
        new_pendings = find_new_pending_trans(pendings, last_known_pendings)
    else:
        new_pendings = pendings

    logger.debug(f'No known pending transactions for {account}')
    message, total = build_message_and_total_for_pending_transactions(account, new_pendings)
    if total:
        subject = 'Pending {total:1.5f} XRB at {account}'.format(total=total, account=account)
        notify(emails, message, subject, from_email='pending@nanotify.co')
        webhook_notify(webhooks, subject, account, total, transaction_type='pending')
        queue_notify(subject, account)
    return pendings


def build_message_and_total_for_new_transactions(account, new_trans):
    account_transactions = defaultdict(list)
    total = 0
    number_of_transactions = 0
    message = None
    for tran in new_trans:
        if tran['type'] == 'receive':
            from_account = tran['account']
            amount = float(tran['amount'])
            hash = tran['hash']
            if amount != 0:
                amount /= 1.0e+30
            total += amount
            number_of_transactions += 1
            account_transactions[from_account].append({'amount': amount, 'hash': hash})
    if total:
        message = render('templates/transactions_email.html', {'transactions': account_transactions, 'account': account,
                                                               'total': total, 'number_of_transactions': number_of_transactions})
    return message, total


def build_message_and_total_for_pending_transactions(account, pendings):
    account_pendings = defaultdict(list)
    total = 0
    number_of_transactions = 0
    message = None
    for hash, tran in pendings.items():
        from_account = tran['source']
        amount = float(tran['amount'])
        if amount != 0:
            amount /= 1.0e+30
        total += amount
        number_of_transactions += 1
        account_pendings[from_account].append({'amount': amount, 'hash': hash})
    if total:
        message = render('templates/pendings_email.html', {'transactions': account_pendings, 'account': account,
                                                           'total': total, 'number_of_transactions': number_of_transactions})
    return message, total


def format_nano(nano):
    return '{nano:1.5f}'.format(nano=nano)


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(path or './'))
    env.filters['format_nano'] = format_nano
    return env.get_template(filename).render(context)
