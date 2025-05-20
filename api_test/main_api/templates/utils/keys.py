import os
from dotenv import load_dotenv

def cargar_secretos_env():
    """Carga variables de entorno desde archivo .env"""
    try:
        load_dotenv()  # Busca automáticamente el archivo .env en el directorio actual
        
        # Verificación básica de variables obligatorias
        required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'BUCKET_NAME']
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"❌ Variable faltante: {var}")

    except Exception as e:
        print(f"Error al cargar variables de entorno: {str(e)}")
        raise

# Cargar secretos al iniciar
cargar_secretos_env()

# Variables accesibles (igual que antes)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Opcional
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Default
BUCKET_NAME = os.getenv('BUCKET_NAME', 'reportesgen')  # Default