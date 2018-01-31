import boto3
import os
from botocore.exceptions import ClientError


source_email = os.getenv('SES_SOURCE_EMAIL')
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)


def send(email_user, subject, message):
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
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': message,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source='raiblockpayments@echosoft.uk',
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
