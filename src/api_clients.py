import requests

# Esto luego cambiará por la URL real del módulo de ventas
BASE_URL_VENTAS = "http://localhost:8000/api/ventas"
BASE_URL_SEGURIDAD = "http://localhost:8001/api/seguridad"
BASE_URL_DESPACHO = "http://localhost:8002/api/despacho"

def obtener_ventas():
    try:
        response = requests.get(f"{BASE_URL_VENTAS}/resumen") # 'resumen' es el endpint escpecífico en donde podemos sacar la info en este ejemplo
        response.raise_for_status() #Con esto verificamos si solicitud fue exitosa (200), si falla va a la excepcion
        return response.json() #transformamos los datos llamados al formato Json
    except requests.RequestException as e:
        print(f"Error al obtener ventas: {e}")
        return [] 

def obtener_seguridad():
    try:
        response = requests.get(f"{BASE_URL_SEGURIDAD}/eventos")  # ejemplo
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos de seguridad: {e}")
        return []

def obtener_despachos():
    try:
        response = requests.get(f"{BASE_URL_DESPACHO}/movimientos")  # ejemplo
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos de despacho: {e}")
        return []
