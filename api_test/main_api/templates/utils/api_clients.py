import requests

# Esto luego cambiará por la URL real del módulo de ventas
BASE_URL_VENTAS = "link de la api"
BASE_URL_SEGURIDAD = "link de la api"
BASE_URL_DESPACHO = "link de la api"
BASE_URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"

def obtener_usuarios():
    try:
        response = requests.get(BASE_URL_USUARIOS)
        response.raise_for_status() # Lanza una excepción para códigos de estado de error (4xx o 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener usuarios: {e}")
        return []

#Dejo base para conectar otras apis
def obtener_ventas():
    try:
        response = requests.get(f"{BASE_URL_VENTAS}/resumen") # 'resumen' es el endpint escpecífico en donde podemos sacar la info en este ejemplo
        response.raise_for_status() #Con esto verificamos si solicitud fue exitosa (200), si falla va a la excepcion

        data_response = response.json

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
