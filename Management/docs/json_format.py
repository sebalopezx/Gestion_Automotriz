import json

def transformar_id(documento):
    if "_id" in documento and "$oid" in documento["_id"]:
        documento["_id"] = documento["_id"]["$oid"]

    if "modelos" in documento:
        for modelo in documento["modelos"]:
            if "_id" in modelo and "$oid" in modelo["_id"]:
                modelo["_id"] = modelo["_id"]["$oid"]
    return documento


# Cargar el JSON
with open('vehiculos.json', 'r') as archivo:
    datos = json.load(archivo)
    datos_transformados = [transformar_id(marca) for marca in datos]

# Guardar los datos transformados en un nuevo archivo
nombre_nuevo_archivo = 'vehiculos_format.json'
with open(nombre_nuevo_archivo, 'w') as nuevo_archivo:
    json.dump(datos_transformados, nuevo_archivo, indent=4)
