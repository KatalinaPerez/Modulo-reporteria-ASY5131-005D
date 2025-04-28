import firebase_admin
from firebase_admin import credentials
import os
from pathlib import Path

ruta_cred = Path(__file__).parent.parent.parent
cred_path = os.path.join(ruta_cred, "config", "serviceAccountKey.json")

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
print("✅ Conexión exitosa a Firebase")


