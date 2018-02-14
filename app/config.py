import os

HOST = os.getenv('RAIBLOCKS_HOST', '[::1]')
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'False') == 'True'
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
TIMEOUT = int(os.getenv('TIMEOUT', 60))
DB_URL = os.getenv('DATABASE_URL')
