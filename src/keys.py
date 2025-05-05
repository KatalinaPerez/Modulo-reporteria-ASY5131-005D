import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Por defecto
BUCKET_NAME = os.getenv('BUCKET_NAME', 'modreporteria')