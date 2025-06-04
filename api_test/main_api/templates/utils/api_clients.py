import requests

BASE_URL_VENTAS = "https://fakestoreapi.com/products"
BASE_URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"
BASE_URL_CONTABILIDAD = "http://34.225.192.85:8000/api/schema/swagger-ui/#/"

def obtener_usuarios():
    try:
        response = requests.get(BASE_URL_USUARIOS)
        response.raise_for_status() # Lanza una excepción para códigos de estado de error (4xx o 5xx)
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener usuarios: {e}")
        return []

#Dejo base para conectar otras apis
def obtener_productos():
    try:
        response = requests.get(f"{BASE_URL_VENTAS}") # 'resumen' es el endpint escpecífico en donde podemos sacar la info en este ejemplo
        response.raise_for_status() #Con esto verificamos si solicitud fue exitosa (200), si falla va a la excepcion
        return response.json() #transformamos los datos llamados al formato Json

    except requests.RequestException as e:
        print(f"Error al obtener productos: {e}")
        return [] 

def obtener_contabilidad():
    try:
        response = requests.get(BASE_URL_CONTABILIDAD)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener contabilidad: {e}")
        return []