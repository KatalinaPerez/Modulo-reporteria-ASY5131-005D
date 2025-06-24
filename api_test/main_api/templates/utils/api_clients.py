import requests
import json
import os
#vienen de apis de internet
BASE_URL_PRODUCTOS = "https://fakestoreapi.com/products"
BASE_URL_USUARIOS = "https://jsonplaceholder.typicode.com/users"

#Apis de nuestro curso
BASE_URL_STOCK = "https://integracionstock-etefhkhbcadegaej.brazilsouth-01.azurewebsites.net/products"
BASE_URL_CONTABILIDAD = "http://34.225.192.85:8000/api/asientoscontables/"
BASE_URL_ADQUISICIONES = "http://35.153.174.128/api/compras/"
BASE_URL_VENTAS = "http://34.238.247.153:8000/api/"
BASE_URL_PROVEEDORES = "http://34.194.212.252/docs/"
BASE_URL_SEGURIDAD = "http://35.168.133.16:3000/login"


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
    '''try:   
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sube a main_api con dirname
        file_path = os.path.join(base_dir, '..', 'static', 'js', 'stock_datos_mock.json')
        file_path = os.path.normpath(file_path)  # normaliza la ruta para cualquier OS

        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al leer el archivo mock: {e}")
        return []'''

def obtener_contabilidad():
    '''try:
        response = requests.get(BASE_URL_CONTABILIDAD)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener contabilidad: {e}")
        return []'''
    try:   
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sube a main_api con dirname
        file_path = os.path.join(base_dir, '..', 'static', 'js', 'cont_datos_mock.json')
        file_path = os.path.normpath(file_path)  # normaliza la ruta para cualquier OS

        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al leer el archivo mock: {e}")
        return []
    
def obtener_adquisiciones():
    '''try:
        response = requests.get(BASE_URL_ADQUISICIONES)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener adquisiciones: {e}")
        return []'''
    try:   
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Sube a main_api con dirname
        file_path = os.path.join(base_dir, '..', 'static', 'js', 'adq_datos_mock.json')
        file_path = os.path.normpath(file_path)  # normaliza la ruta para cualquier OS

        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error al leer el archivo mock: {e}")
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
    
