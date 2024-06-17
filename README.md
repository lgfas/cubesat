# Sensor de Temperatura e Publicação MQTT

Este projeto consiste em um script Python para medir a temperatura usando o sensor SHT20 e publicar os dados em um tópico MQTT. Além disso, vou fornecer instruções sobre como integrar esses dados a um recurso específico usando uma API.

## Pré-requisitos

- Hardware:

  - ESP32 (ou outro dispositivo compatível)
  - Sensor SHT20 (ou similar)
  - Conexão Wi-Fi

- Software:
  - Python 3.x
  - Bibliotecas: umqtt.robust, network, time, machine, I2C

## Configuração

1. _Conexão do Sensor SHT20:_

   - Conecte o sensor SHT20 ao ESP32 usando os pinos SDA (data) e SCL (clock) para comunicação I2C.

2. _Configuração Wi-Fi:_

   - No código, substitua o nome da rede Wi-Fi ('motog52_3718') e a senha ('12345678') pelas suas próprias credenciais.

3. _Configuração MQTT:_
   - Defina o servidor MQTT (por exemplo, "bipes.net.br") e as credenciais (usuário e senha) no código.

## Executando o Script

1. Carregue o código no ESP32.
2. O dispositivo se conectará à rede Wi-Fi e começará a ler a temperatura do sensor SHT20.
3. Os dados de temperatura serão publicados no tópico MQTT especificado.

## Integração com Recurso

1. _Leitura do Arquivo CSV:_

   - Certifique-se de ter o arquivo CSV (temperatures.csv) na raiz do projeto.

2. _Atualização do Dicionário capability_data_json:_

   - Use o código fornecido para ler o arquivo CSV e atualizar o dicionário capability_data_json com as temperaturas e timestamps.

3. _Envio dos Dados para o Recurso:_
   - Faça uma solicitação POST para o recurso desejado com os dados atualizados.

## Exemplo de Uso

python

# Exemplo de uso para atualizar o dicionário capability_data_json

# (Adicione este trecho ao seu código)

import csv
import requests

# Ler o arquivo CSV

csv_file = 'temperatures.csv'
capability_data_json = {"data": []}

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

Lembre-se de ajustar as variáveis conforme o seu ambiente específico.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para obter mais detalhes.

---
