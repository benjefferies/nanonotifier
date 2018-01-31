import boto3
import os
from botocore.exceptions import ClientError


AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)


def send(email_user, subject, message):
    email_domain = email_user.split("@")[1]
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
                        '"UTF-8"': "UTF-8",
                        'Data': message,
                    },
                },
                'Subject': {
                    '"UTF-8"': "UTF-8",
                    'Data': subject,
                },
            },
            Source=f'raiblockpayments@{email_domain}',
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
