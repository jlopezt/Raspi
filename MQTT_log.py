import time
import os

import datetime
import logging

import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from influxdb import InfluxDBClient

# Informacion sobre el bus MQTT
Broker_IP = "10.68.1.100"
Broker_Puerto = 1883
sub_topic = "casa/+/medidas"    # receive messages on this topic
pub_topic = "casa/monitor"      # send messages to this topic

#Informacion de la base de datos InfluxDB
DB_IP = "10.68.1.100"
DB_Puerto = 8086
BaseDatos = 'casa'
Measurement = 'termostatix'

print("Iniciando ejecucion...")

#inicializamos la DB
clienteInflux = InfluxDBClient(host=DB_IP, port=DB_Puerto, database=BaseDatos)
print("Conectado: " + str(clienteInflux.ping()))

# mqtt section

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Conectado al bus con el codigo de resultado "+str(rc))
    client.subscribe(sub_topic)
    print("Suscrito al topic ",sub_topic)
    #publish_mqtt("Conectrado al bus...")

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
    print(" ");
    print("-----------------------------------------------------");

    print("recibido= "+msg.topic+" "+msg.payload)
    decoded = json.loads(msg.payload)

    #preparo los datos para el json
    current_time = datetime.datetime.utcnow().isoformat()
    #current_time = datetime.datetime.now().isoformat()
    id=decoded["id"]
    temperatura= decoded["Temperatura"]
    humedad= decoded["Humedad"]
    luz= decoded["Luz"]

    #leo la habitacion
    cadena=str(msg.topic)
    habitacion = cadena.split("/")[1]

    json_body = [
        {
        "measurement": Measurement,
        "tags": {
            "id": id,
            "habitacion": habitacion,
            "topic": str(msg.topic)
            },
        "time": current_time,
        "fields": {
            "Temperatura": temperatura,
            "Humedad": humedad,
            "Luz": luz
            }
        }
    ]

    print(" ");
    print(json_body)
    if not clienteInflux.write_points(json_body): 
    	print ("Error al insertar datos")
    print("-----------------------------------------------------");

# to send a message

def publish_mqtt(sensor_data):
    mqttc = mqtt.Client("monitor_Raspi")
    mqttc.connect(Broker_IP, Broker_Puerto)
    mqttc.publish(pub_topic, sensor_data)
    #mqttc.loop(2) //timeout = 2s

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker_IP, Broker_Puerto, 60)
client.loop_forever()
