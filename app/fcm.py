import logging

from pyfcm import FCMNotification

from app.config import FCM_API_KEY

logger = logging.getLogger(__name__)


def send(account, subject):
    push_service = FCMNotification(api_key=FCM_API_KEY)
    push_service.notify_topic_subscribers(topic_name=account, message_body=subject)
