import pyrebase

config = {
    "apiKey": "AIzaSyCiJ_ZzIDRP2j2jSz_uq1O11bY-kB-tr5Q",
    "authDomain": "reportes-41ce0.firebaseapp.com",
    "databaseURL": "https://reportes-41ce0-default-rtdb.firebaseio.com/",
    "storageBucket": "reportes-41ce0.firebasestorage.app"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def obtener_reporte(id_reporte):
    reporte_data = db.child("reportes").child(id_reporte).get().val()
    return reporte_data