import os
import json
import subprocess

def cargar_secretos_doppler():
    try:
        # Ejecutar el comando de Doppler para obtener los secretos en formato JSON
        resultado = subprocess.run(
            ["doppler", "secrets", "download", "--no-file", "--format", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        secretos = json.loads(resultado.stdout)

        # Establecer cada secreto como una variable de entorno
        for clave, valor in secretos.items():
            os.environ[clave] = valor

    except subprocess.CalledProcessError as e:
        print("❌ Error al cargar secretos desde Doppler:", e.stderr)
    except json.JSONDecodeError:
        print("❌ Error al parsear los secretos de Doppler.")

# Cargar secretos al entorno antes de usarlos
cargar_secretos_doppler()

# Variables de entorno disponibles en el código
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN')  # Puedes ignorarlo si no lo usas
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1')  # Valor por defecto
BUCKET_NAME = os.getenv('BUCKET_NAME', 'modreporteria')  # Valor por defecto
