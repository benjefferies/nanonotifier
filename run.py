import logging
import time
from collections import defaultdict

from app.config import TIMEOUT
from app.models import Subscription, session
from app.nano import check_account_for_new_transactions, check_account_for_new_pending, get_pendings

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    last_known_trans = defaultdict(str)
    last_known_pending = defaultdict(dict)

    # Initialise pendings before notifying
    for subscription in session.query(Subscription):
        last_known_pending[subscription.account] = get_pendings(subscription.account)
    while True:
        subToEmails = defaultdict(list)
        subToHttps = defaultdict(list)
        logger.info('Loading email subscriptions')

        # Map account to emails and HTTP addresses
        for subscription in session.query(Subscription):
            subToEmails[subscription.account].append(subscription.email)
            subToHttps[subscription.account].append(subscription.http)

        for account in subToEmails.keys():
            logger.info(f'Checking for new transactions for {account}')
            emails = subToEmails[account]
            https = subToHttps[account]
            account_last_known_trans = last_known_trans[account]
            last_known_trans[account] = check_account_for_new_transactions(account, account_last_known_trans, emails, https)
            last_known_pending[account] = check_account_for_new_pending(account, last_known_pending[account], emails, https)
        time.sleep(TIMEOUT)
