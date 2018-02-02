import logging
import os
import time
from collections import defaultdict

from app.models import Subscription, session
from app.nano import check_account

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    last_known_trans = defaultdict(list)
    while True:
        subToEmails = defaultdict(list)
        logger.info('Loading email subscriptions')

        # Map account to emails
        for subscription in session.query(Subscription):
            subToEmails[subscription.account].append(subscription.email)

        for account in subToEmails.keys():
            logger.info(f'Checking for new transactions for {account}')
            emails = subToEmails[account]
            account_last_known_trans = last_known_trans[account]
            last_known_trans[account] = check_account(account, account_last_known_trans, emails)
        time.sleep(int(os.getenv('TIMEOUT', 60)))
