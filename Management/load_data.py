# import csv
# from pathlib import Path
# import os

# Obtén las rutas de los archivos CSV en el mismo directorio que este script
# current_directory = os.path.dirname(os.path.abspath(__file__))
# marcas_file = os.path.join(current_directory, 'marcas.csv')
# modelos_file = os.path.join(current_directory, 'modelos.csv')
# years_file = os.path.join(current_directory, 'anios.csv')

# # Lista para almacenar los datos de los archivos CSV
# data = []

# # Cargar datos de 'marcas.csv'
# with open(marcas_file, 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         data.append({'brand': row['make']})

# # Cargar datos de 'modelos.csv'
# with open(modelos_file, 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         # Suponiendo que 'modelos.csv' tiene una columna llamada 'model'
#         data.append({'model': row['model']})

# # Cargar datos de 'years.csv'
# with open(years_file, 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         data.append({'year': row['year']})

# Imprimir los datos para verificar
# print(data)

# class CSVDataProvider:
#     def __init__(self):
#         self.data_path = Path(__file__).resolve().parent / 'data'
#         self.brands_file = self.data_path / 'marcas.csv'
#         self.models_file = self.data_path / 'modelos.csv'
#         self.years_file = self.data_path / 'anios.csv'

#     def get_brand_choices(self):
#         with open(self.brands_file, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             return [('', 'Elegir marca vehículo')] + [(row['slug'], row['make']) for row in reader]

#     def get_model_choices(self, brand_slug):
#         models = []
#         with open(self.models_file, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['idmake'] == brand_slug:
#                     models.append((row['id'], row['model']))
#         return [('', 'Elegir modelo vehículo')] + models

#     def get_year_choices(self, model_id):
#         with open(self.years_file, 'r') as file:
#             reader = csv.DictReader(file)
#             return [(row['id'], row['year']) for row in reader if row['idmodel'] == str(model_id)]



# csv_files = ['marcas.csv', 'modelos.csv', 'anios.csv']

# data = []

# for csv_file in csv_files:
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)
#         data.extend(list(reader))

# print(data)
