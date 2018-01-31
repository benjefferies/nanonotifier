from collections import defaultdict

from app.models import Notification, session
from app.nano import get_trans_history, check_account


def notifications():
    notification = Notification()
    notification.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
    notification.email = 'benjjefferies@gmail.com'
    session.add(notification)

    notification = Notification()
    notification.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
    notification.email = 'jack.h.jefferies@gmail.com'
    session.add(notification)

    notification = Notification()
    notification.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
    notification.email = 'benjefferies@echosoft.uk'
    session.add(notification)
    session.commit()


if __name__ == '__main__':
    notifications()
    notificationToEmails = defaultdict(list)
    for notification in session.query(Notification):
        notificationToEmails[notification.account].append(notification.email)

    last_known_trans = {}
    for account in notificationToEmails.keys():
        last_known_trans[account] = get_trans_history(account)

    while True:
        for account in last_known_trans.keys():
            account_last_known_trans = last_known_trans[account]
            emails = notificationToEmails[account]
            last_known_trans[account] = check_account(account, account_last_known_trans, emails)
