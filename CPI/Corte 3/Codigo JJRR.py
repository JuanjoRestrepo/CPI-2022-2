from pyModbusTCP.client import ModbusClient # Modbus TCP Client
import time
import redis
import json

# TCP auto connect on modbus request, close after it
client = ModbusClient (host="10.70.28.96", port=502)

r = redis.Redis(
  host='redis-19099.c100.us-east-1-4.ec2.cloud.redislabs.com',
  port=19099,
  password='WpbKZur4yHUgNbntzdJvEGuU3FRoDlZR')

nombre = {
    "maxlevel": 300
}

process_data = {
    "level" : 100,
    "SetPoint" : 145,
}

tank_model = {
    "nombre" : nombre,
    "process_data" : process_data
}

r.json().set("tank", ".", tank_model)


while True:
    Nivel = client.read_holding_registers(0)
    SetPoint = client.read_holding_registers(2)

    if Nivel:

        nivelFinal = (300*Nivel[0])/1000
        SetPointFinal = (300*SetPoint[0])/1000

        r.json().set("tank", ".process_data.level", nivelFinal)
        r.json().set("tank", ".process_data.SetPoint", SetPointFinal)

        time.sleep(2)
    else:
        print("Unable to read registers")
