import sys, getopt
import time
import os

import datetime
import logging

import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from influxdb import InfluxDBClient

import config


def main(argv):
    configFile = ''
    outputFile = ''
    print(argv)
    try:
        opts, arg = getopt.getopt(argv,"i:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'MQTT_log.py -c <configfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            configFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
    print 'Iniciando con fichero de configuracion "', configFile
    print 'Salida direccionda a "', outputFile

    #if __name__ == "__main__":
    #   main(sys.argv[1:])

    #leo la configuracion
    config=config.Configuracion('MQTT_log.config.json',True)

    print("Iniciando ejecucion...")

    #inicializamos la DB
    clienteInflux = InfluxDBClient(host=config.getDB_IP(), port=config.getDB_Puerto(), database=config.getBaseDatos())
    print("Conectado: " + str(clienteInflux.ping()))

    # mqtt section

    # when connecting to mqtt do this;

    def on_connect(client, userdata, flags, rc):
        print("Conectado al bus con el codigo de resultado "+str(rc))
        client.subscribe(config.getsub_topic())
        print("Suscrito al topic ",config.getsub_topic())
        #publish_mqtt("Conectrado al bus...")

    # when receiving a mqtt message do this;

    def on_message(client, userdata, msg):
        print(" ")
        print("Init -----------------------------------------------------")
        try:
            print("recibido= %s %s" %(msg.topic,msg.payload))
            decoded = json.loads(msg.payload)
        except:
            print("error al pintar el mensaje recibido.")

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
            "measurement": config.getMeasurement(),
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

        print(" ")
        print(json_body)
        if not clienteInflux.write_points(json_body): 
            print ("Error al insertar datos")
        print("Fin  -----------------------------------------------------")

    # to send a message

    def publish_mqtt(sensor_data):
        mqttc = mqtt.Client("monitor_Raspi")
        mqttc.connect(config.getBroker_IP(), config.getBroker_Puerto())
        mqttc.publish(config.getpub_topic(), sensor_data)
        #mqttc.loop(2) //timeout = 2s

    def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.getBroker_IP(), config.getBroker_Puerto(), 60)
    client.loop_forever()

if __name__ == "__main__":
   main(sys.argv[1:])    
