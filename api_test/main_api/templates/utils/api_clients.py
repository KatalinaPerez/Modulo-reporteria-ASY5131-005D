import requests
#vienen de apis de internet
BASE_URL_PRODUCTOS = "https://fakestoreapi.com/products"
BASE_URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"

#Apis de nuestro curso
BASE_URL_STOCK = "aun no la pasan, pero sabemos la structura"
BASE_URL_CONTABILIDAD = "http://34.225.192.85:8000/api/schema/swagger-ui/#/"
BASE_URL_ADQUISICIONES = "http://35.153.174.128/api/compras/"
BASE_URL_VENTAS = "http://34.238.247.153:8000/api/"
BASE_URL_PROVEEDORES = " http://34.194.212.252/docs/"

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
        response = requests.get(f"{BASE_URL_PRODUCTOS}") # 'resumen' es el endpint escpecífico en donde podemos sacar la info en este ejemplo
        response.raise_for_status() #Con esto verificamos si solicitud fue exitosa (200), si falla va a la excepcion
        return response.json() #transformamos los datos llamados al formato Json

    except requests.RequestException as e:
        print(f"Error al obtener productos: {e}")
        return [] 

def obtener_stock():
    try:
        response = requests.get(BASE_URL_STOCK)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener stock: {e}")
        return []

def obtener_contabilidad():
    try:
        response = requests.get(BASE_URL_CONTABILIDAD)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener contabilidad: {e}")
        return []
    
def obtener_adquisiciones():
    try:
        response = requests.get(BASE_URL_ADQUISICIONES)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener adquisiciones: {e}")
        return []

def obtener_ventas():
    try:
        response = requests.get(BASE_URL_VENTAS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener ventas: {e}")
        return []
    
def obtener_proveedores():
    try:
        response = requests.get(BASE_URL_PROVEEDORES)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener proveedores: {e}")
        return []
    
