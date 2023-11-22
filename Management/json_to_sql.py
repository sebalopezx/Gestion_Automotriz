# import json

# with open('data.json', 'r') as json_file:
#     data = json.load(json_file)

# with open('data.sql', 'w') as sql_file:
#     for entry in data:
#         model = entry['model']
#         fields = entry['fields']
#         columns = ', '.join(fields.keys())
#         values = ', '.join(['"{}"'.format(val) for val in fields.values()])
#         sql = f'INSERT INTO {model} ({columns}) VALUES ({values});\n'
#         sql_file.write(sql)
