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
#Chapuza a corregir
OK                          =  0
CONFIGURACION_POR_DEFECTO   = -1
ERROR_FICHERO_CONFIGURACION = -2

###########   MAIN   #################
def main(argv):
    configFile = ''
    outputFile = ''
    verbose = False

    try:
        opts, arg = getopt.getopt(argv,"hvi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'MQTT_log.py -c <configfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ''
            print 'MQTT_log.py -c <configFile> -o <outputfile> -h -v'
            print '-i <configFile> fichero de configuracion'
            print '-o <outputFile> fichero de salida. Si no existe se creara, si existe se anadiran lineas al final'
            print '-h esta ayuda'
            print '-v verbose mode'            
            print ''
            sys.exit()
        elif opt == "-v":
            verbose = True
        elif opt in ("-i", "--ifile"):
            configFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
    print('Iniciando con fichero de configuracion [%s]' %configFile)
    print('Salida direccionda a [%s]' %outputFile)

    #leo la configuracion
    localConfig=config.Configuracion(configFile, verbose)
    if (localConfig.getConfigurado()==ERROR_FICHERO_CONFIGURACION): 
        print("No se pudo leer el fichero de configuracion")
        sys.exit()
    elif (localConfig.getConfigurado()==CONFIGURACION_POR_DEFECTO): 
        print("Faltan parametros en el fichero de configuracion")
        sys.exit()    

    #inicializo el fichero de salida
    print("Configurando fichero de salida")
    if (outputFile == ''): verbose==True
    else:
        try:
            f = open (outputFile,"at")
        except:
            print("Error al abrir el fichero de salida")
            sys.exit()        

    #inicializamos la DB
    print("Iniciando la base de datos")
    clienteInflux = InfluxDBClient(host=localConfig.getDB_IP(), port=localConfig.getDB_Puerto(), database=localConfig.getBaseDatos())
    if (verbose): print("Conectado: " + str(clienteInflux.ping()))


    print("Iniciando MQTT")
    ########################################################################################
    # mqtt section
    # when connecting to mqtt do this;
    def on_connect(client, userdata, flags, rc):
        if (verbose): print("Conectado al bus con el codigo de resultado "+str(rc))
        client.subscribe(localConfig.getsub_topic())
        if (verbose): print("Suscrito al topic ",localConfig.getsub_topic())
        #publish_mqtt("Conectrado al bus...")

    # when receiving a mqtt message do this;
    def on_message(client, userdata, msg):
        if (verbose): print("\nInit -----------------------------------------------------")
        try:
            if (verbose): print("recibido= %s %s" %(msg.topic,msg.payload))
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
            "measurement": localConfig.getMeasurement(),
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

        cad = str(json_body)+"\n"
        if (verbose): print("\n%s" %cad)

        #Salida a fichero
        f = open(outputFile, "at")
        f.write(cad)
        f.close()

        if not clienteInflux.write_points(json_body): 
            print ("Error al insertar datos")
        if (verbose): print("Fin  -----------------------------------------------------")

    # to send a message
    def publish_mqtt(sensor_data):
        mqttc = mqtt.Client("monitor_Raspi")
        mqttc.connect(localConfig.getBroker_IP(), localConfig.getBroker_Puerto())
        mqttc.publish(localConfig.getpub_topic(), sensor_data)
        #mqttc.loop(2) //timeout = 2s

    def on_publish(mosq, obj, mid):
        if (verbose): print("mid: " + str(mid))
    ########################################################################################

    #iniciando MQTT
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(localConfig.getBroker_IP(), localConfig.getBroker_Puerto(), 60)

    print("Iniciando ejecucion...")

    client.loop_forever()


if __name__ == "__main__":
   main(sys.argv[1:])    
