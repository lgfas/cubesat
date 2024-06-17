import requests
import json
import csv

# Endereço para a api
api = 'http://cidadesinteligentes.lsdi.ufma.br'

# Cria uma 'capability'

# Playground - Resource Catalog - Post - Catalog capabilities

capability_json = {
  "name": "temperatura",
  "description": "Mede a temperatura do ambiente em graus Celsius",
  "capability_type": "sensor"
}
r = requests.post(api+'/catalog/capabilities/', json=capability_json)
if(r.status_code == 201):
  content = json.loads(r.text)
  print(json.dumps(content, indent=2, sort_keys=True))
else:
  print('Status code: '+str(r.status_code))


# Exibe as 'capabilities'

# Playground - Resource Catalog - Get - Catalog capabilities

r = requests.get(api+'/catalog/capabilities')
if(r.status_code == 200):
  content = json.loads(r.text)
  print(json.dumps(content, indent=2, sort_keys=True))
else:
  print('Status code: '+str(r.status_code))


# Cria um 'resource'

# Playground - Resource Catalog - Post - Catalog resource

resource_json = {
  "data": {
    "description": "Cubesat",
    "capabilities": [
      "temperatura"
    ],
    "status": "active",
    "lat": -23.559616,
    "lon": -46.731386
  }
}
r = requests.post(api+'/catalog/resources', json=resource_json)
uuid = ''
if(r.status_code == 201):
  resource = json.loads(r.text)
  uuid = resource['data']['uuid']
  print(json.dumps(resource, indent=2))
else:
  print('Status code: '+str(r.status_code))


# Exibe os 'resources'

# Playground - Resource Catalog - Get - Catalog resource

r = requests.get(api+'/catalog/resources')
if(r.status_code == 200):
  content = json.loads(r.text)
  print(json.dumps(content, indent=2, sort_keys=True))
else:
  print('Status code: '+str(r.status_code))




# Ler o arquivo CSV (supondo que o arquivo esteja na raiz)
csv_file = 'temperatures.csv'

# Inicializar o dicionário capability_data_json
capability_data_json = {
    "data": []
}

# Abrir o arquivo CSV e ler as temperaturas
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        if 'temperatura' in row:
            temperatura = float(row['temperatura'])
            timestamp = row['timestamp']
            capability_data_json['data'].append({
                "temperatura": temperatura,
                "timestamp": timestamp
            })

# Fazer a solicitação POST para o recurso
url = f"{api}/adaptor/resources/{uuid}/data/environment_monitoring"
r = requests.post(url, json=capability_data_json)

if r.status_code == 201:
    print('Ok')
else:
    print(f'Status code: {r.status_code}')

# Exibe dados do 'resource'

# Playground - Data collector - Post - Resources data

r = requests.post(api+'/collector/resources/'+uuid+'/data')
if(r.status_code == 200):
  content = json.loads(r.text)
  print(json.dumps(content, indent=2, sort_keys=True))
else:
  print('Status code: '+str(r.status_code))