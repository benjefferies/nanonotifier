import logging
import time
from collections import defaultdict

import os

from app.models import Notification, session
from app.nano import get_trans_history, check_account

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    notificationToEmails = defaultdict(list)
    logger.info('Loading notifications')
    for notification in session.query(Notification):
        notificationToEmails[notification.account].append(notification.email)

    last_known_trans = {}
    for account in notificationToEmails.keys():
        logger.info(f'Getting transaction history for {account}')
        last_known_trans[account] = get_trans_history(account)

    while True:
        for account in last_known_trans.keys():
            logger.info(f'Checking for new transactions for {account}')
            account_last_known_trans = last_known_trans[account]
            emails = notificationToEmails[account]
            last_known_trans[account] = check_account(account, account_last_known_trans, emails)
        time.sleep(int(os.getenv('TIMEOUT', 5)))
