#!/usr/bin/python3
import json
import signal
import requests

MAIN_URL = 'https://consultasimit2.fcm.org.co/simit/microservices/estado-cuenta-simit/estadocuenta/consulta'

def signal_handler(sig, frame):
  print('\n\nYou pressed Ctrl+C!, exiting\n')
  exit(1)

signal.signal(signal.SIGINT, signal_handler)

def make_request(placa: str) -> dict:

  data_post = {"filtro":placa,"reCaptchaDTO":{"response":"[{\"question\":\"62c16040f13b79f35e71044ae60fd145\",\"time\":1711934267,\"nonce\":179269}]","consumidor":"1"}}

  headers_data = {
    'Content-Type':'application/json',
    'User-Agent': 'Windows 12'
  }

  r = requests.post(url=MAIN_URL, json=data_post, headers=headers_data).json()

  return r

def get_data(json_response: dict) -> dict:


  if len(json_response['multas']) == 0:
      return 'NO TIENE MULTAS'

  multas_list = json_response.get('multas')

  final_multas = []

  for multa in multas_list:
    
    temp_multa_info = {
      'cod_infraccion': multa.get('infracciones')[0].get('codigoInfraccion'),
      'descripcion': multa.get('infracciones')[0].get('descripcionInfraccion'),
      'organismo_transito': multa.get('organismoTransito'),
      'departamento': multa.get('departamento'),
      'valor_multa': multa.get('valorPagar'),
      'fecha_multa': multa.get('fechaComparendo'),
      'estado': multa.get('estadoCartera')
    }

    final_multas.append(temp_multa_info)


  return {
    'info_conductor': {
       'NOMBRE_COMPLETO': json_response.get('multas')[0].get('infractor').get('nombre') + json_response.get('multas')[0].get('infractor').get('apellido'),
       'CEDULA': json_response.get('multas')[0].get('infractor').get('numeroDocumento')
    },
    'placa': json_response.get('multas')[0].get('placa'),
    'numero_de_multas': len(json_response.get('multas')),
    'total_a_pagar': json_response.get('totalGeneral'),
    'multas': final_multas
  }


def main(placa: str):

  response = make_request(placa=placa)

  data = get_data(response)

  print(json.dumps(data, indent=3))

if __name__ == '__main__':

  placa = input('Placa o numero de documento: ').upper()

  main(placa)
