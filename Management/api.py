# import requests
# from django.conf import settings
# from django.http import JsonResponse

# def obtener_marcas_y_modelos(request):
#     api_key = settings.EDMUNDS_API_KEY
#     url = f'https://api.edmunds.com/api/vehicle/v2/makes?fmt=json&api_key={api_key}'

#     response = requests.get(url)
#     data = response.json()

#     return JsonResponse(data)

# import_data.py

# import csv
# from .models import Brand, Model, Year

# def import_data(csv_file, model_class):
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             model_class.objects.create(**row)

# # Ejemplos de llamadas
# import_data('brands.csv', Brand)
# import_data('models.csv', Model)
# import_data('years.csv', Year)

# serializers.py

from rest_framework import serializers

class VehicleDataSerializer(serializers.Serializer):
    brand = serializers.CharField()
    model = serializers.CharField()
    year = serializers.IntegerField()

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
# from .load_data import data 
from django.http import JsonResponse
import json
# from .serializers import VehicleDataSerializer

class VehicleDataAPIView(APIView):
    def get(self, request):
        # Aquí puedes cargar los datos en memoria desde los archivos CSV
        # y convertirlos en una estructura de datos que puedas serializar.
        # data = [
        #     {"brand": "Toyota", "model": "Camry", "year": 2022},
        #     {"brand": "Ford", "model": "Focus", "year": 2021},
        #     # ... más datos ...
        # ]
        pass
        # serializer = VehicleDataSerializer(data, many=True)
        # return Response(serializer.data)

def obtener_marcas_y_modelos(request):
    # Tu lógica para obtener los datos de las marcas y modelos
    # data = []  # Esta es tu lista de datos
    # print(data)
    # Serializar los datos a JSON
    # json_data = json.dumps(data)

    # # Devolver la respuesta JSON
    # return JsonResponse(json_data, safe=False)
    pass