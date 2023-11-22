# import csv
# from pathlib import Path
# import os

# # Obtén las rutas de los archivos CSV en el mismo directorio que este script
# current_directory = os.path.dirname(os.path.abspath(__file__))
# marcas_file = os.path.join(current_directory, 'marcas.csv')
# modelos_file = os.path.join(current_directory, 'modelos.csv')
# years_file = os.path.join(current_directory, 'years.csv')

# # Lista para almacenar los datos de los archivos CSV
# data = []

# # Cargar datos de 'marcas.csv'
# with open(marcas_file, 'r') as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         data.append({'brand': row['brand']})

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

# # Imprimir los datos para verificar
# print(data)




# csv_files = ['marcas.csv', 'modelos.csv', 'anios.csv']

# data = []

# for csv_file in csv_files:
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)
#         data.extend(list(reader))

# print(data)
