import os
import json
import subprocess
from dotenv import load_dotenv


load_dotenv()

# Variables de entorno disponibles en el código
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Puedes ignorarlo si no lo usas
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Valor por defecto
BUCKET_NAME = os.getenv('BUCKET_NAME', 'modreporteria')  # Valor por defecto
