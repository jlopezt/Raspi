import time
import os

import datetime
import logging

import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from influxdb import InfluxDBClient

# Informacion sobre el bus MQTT
Broker = "10.68.1.100"
sub_topic = "casa/will"    # receive messages on this topic
pub_topic = "casa/monior"

#Informacion de la base de datos InfluxDB
DB_IP = "10.68.1.100"
Puerto = 8086
BaseDatos = 'casa'
Measurement = 'will'

#inicializamos la DB
clienteInflux = InfluxDBClient(host=DB_IP, port=Puerto, database=BaseDatos)
print("Conectado: " + str(clienteInflux.ping()))

# mqtt section

# when connecting to mqtt do this;
def on_connect(client, userdata, flags, rc):
    print("Conectado al bus con el codigo de resultado "+str(rc))
    client.subscribe(sub_topic)
    publish_mqtt("Conectrado al bus...")

# when receiving a mqtt message do this;
def on_message(client, userdata, msg):
    print("recibido= "+msg.topic+" "+msg.payload)

		#preparo los datos para el json    
    current_time = datetime.datetime.utcnow().isoformat()
    
    json_body = [
        {
        "measurement": Measurement,
        "tags": {
            },
        "time": current_time,
        "fields": {
            "mensaje": msg.payload
            }
        }
    ]
    
    print(json_body)
    if not clienteInflux.write_points(json_body): 
    	print ("Error al insertar datos")

# to send a message
def publish_mqtt(sensor_data):
    mqttc = mqtt.Client("monitor_Raspi")
    mqttc.connect(Broker, 1883)
    mqttc.publish(pub_topic, sensor_data)
    #mqttc.loop(2) //timeout = 2s

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, 1883, 60)
client.loop_forever()
