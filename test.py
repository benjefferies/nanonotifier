import logging

from app.models import Notification, session

logger = logging.getLogger(__name__)

logger.info('Inserting notifications')
notification = Notification()
notification.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
notification.email = 'benjjefferies@gmail.com'
session.add(notification)

notification = Notification()
notification.account = 'xrb_3xjnmhz5oc1p6oabo15a33nuu86uwwx87f3qot36eax73ous6ez9ytdoyrcr'
notification.email = 'benjefferies@echosoft.uk'
session.add(notification)
session.commit()