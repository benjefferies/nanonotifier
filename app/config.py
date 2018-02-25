import os

HOST = os.getenv('RAIBLOCKS_HOST', '[::1]')
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False') == 'True'
WEBHOOK_ENABLED = os.getenv('WEBHOOK_ENABLED', 'False') == 'True'
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
TIMEOUT = int(os.getenv('TIMEOUT', 60))
WEBHOOK_TIMEOUT = int(os.getenv('TIMEOUT', 0.5))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///test.db')
