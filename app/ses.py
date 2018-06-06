import logging

import boto3
from botocore.exceptions import ClientError

# Create a new SES resource and specify a region.
from app.config import AWS_REGION


logger = logging.getLogger(__name__)


def send(email_user, subject, message, from_email):
    client = boto3.client('ses', region_name=AWS_REGION)
    logger.info(f'Sending email to {email_user} with subject {subject}')
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email_user,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': message,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=from_email,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.exception(e.response['Error']['Message'])
    else:
        logger.debug("Email sent! Message ID:"),
        logger.debug(response['ResponseMetadata']['RequestId'])
