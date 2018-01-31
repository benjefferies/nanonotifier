import logging

from app.models import Subscription, session

logger = logging.getLogger(__name__)

logger.info('Inserting subscription')
subscription = Subscription()
subscription.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
subscription.email = 'benjjefferies@gmail.com'
session.add(subscription)

subscription = Subscription()
subscription.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
subscription.email = 'benjefferies@echosoft.uk'
session.add(subscription)
session.commit()