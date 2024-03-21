from django.http import JsonResponse
import requests
import os, json
from Project.settings import BASE_DIR

"""
TEST :
para obtener data json desde API
desde Python para optar por opcion de csv en caso de fallar API
"""


URL_API = "https://apicardetails-production.up.railway.app/vehiculos"
JSON_VEHICULOS_TRANSFORMADOS = os.path.join(BASE_DIR, 'vehiculos_transformados.json')


def api_vehicles():
    try:
        response = requests.get(URL_API)
        response.raise_for_status()  # Esto lanzará una excepción si el código de estado no es 200
        datos = response.json()
        # return datos
        return JsonResponse(datos, safe=False)
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return JsonResponse({'error': 'No se pudo obtener los datos'}, status=500)


def get_brands():
    try:
        response = requests.get(URL_API)
        response.raise_for_status()  # Asegura que la respuesta sea 200 OK
        datos = response.json()
        # Suponiendo que datos es una lista de objetos de marca, donde cada uno tiene un 'marca' y '_id'
        return datos
        # marcas = [(marca['_id'], marca['marca']) for marca in datos]
        # return JsonResponse(marcas, safe=False)
        # return marcas
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return cargar_marcas_desde_json()
    


def get_models(request, object_id_marca):
    try:
        response = requests.get(URL_API)
        response.raise_for_status()
        marcas = response.json()
        modelos = next((marca['modelos'] for marca in marcas if marca['_id'] == object_id_marca), [])
        return JsonResponse(modelos, safe=False)
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return JsonResponse( cargar_modelos_desde_json(object_id_marca) , safe=False)
    except Exception as e:
        print(f"Otro error al obtener modelos: {e}")
        return JsonResponse( cargar_modelos_desde_json(object_id_marca) , safe=False)
   

def get_years(request, object_id_marca, object_id_modelo):
    try:
        response = requests.get(URL_API)
        response.raise_for_status()
        marcas = response.json()
        for marca in marcas:
            if marca['_id'] == object_id_marca:
                for modelo in marca.get('modelos', []):
                    if modelo['_id'] == object_id_modelo:
                        anios = modelo.get('anios', [])
                        return JsonResponse(anios, safe=False)
        return JsonResponse({'error': 'Marca o modelo no encontrado'}, status=404)
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return JsonResponse( cargar_anios_desde_json(object_id_marca, object_id_modelo), safe=False)
    except Exception as e:
        print(f"Otro error al obtener años: {e}")
        return JsonResponse( cargar_anios_desde_json(object_id_marca, object_id_modelo), safe=False)
    

def cargar_marcas_desde_json():
    ruta_json = os.path.join(BASE_DIR, 'vehiculos_format.json')
    try:
        with open(ruta_json, 'r') as archivo:
            datos = json.load(archivo)
            return [(marca['_id'], marca['marca']) for marca in datos]  # Asume que tus marcas tienen estos campos
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_json}")
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en: {ruta_json}")
    return []

def cargar_modelos_desde_json(id_marca):
    ruta_json = os.path.join(BASE_DIR, 'vehiculos_format.json')
    try:
        with open(ruta_json, 'r') as archivo:
            datos = json.load(archivo)
            for marca in datos:
                if marca['_id'] == id_marca:
                    modelos = marca.get('modelos', [])
                    return modelos
                
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_json}")
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en: {ruta_json}")
    return []

def cargar_anios_desde_json(id_marca, id_modelo):
    ruta_json = os.path.join(BASE_DIR, 'vehiculos_format.json')
    try:
        with open(ruta_json, 'r') as archivo:
            datos = json.load(archivo)
            for marca in datos:
                if marca['_id'] == id_marca:
                    for modelo in marca.get('modelos', []):
                        if modelo['_id'] == id_modelo:
                            anios = modelo.get('anios', [])
                            return anios
                        
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_json}")
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON en: {ruta_json}")
    return []









def get_models_by_brand(request, brand_slug):
    # Suponiendo que `vehicle_data` es la lista que contiene toda la información de vehículos
    vehicle_data = get_brands()

    # Encuentra la marca correspondiente por su slug
    for brand in vehicle_data:
        if brand['slugmarca'] == brand_slug:
            # Extrae los modelos para esa marca y devuelve como respuesta JSON
            models = [{'modelo': model['modelo'], 'slugmodelo': model['slugmodelo']} for model in brand['modelos']]
            return JsonResponse({'models': models})

    return JsonResponse({'models': []})