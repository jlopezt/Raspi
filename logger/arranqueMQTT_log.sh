#!/bin/bash

##Replicado del bus de Rapi2. ELIMINAR TRAS LA MIGRACION
#nohup python /opt/monitorMQTT/MQTT_gw.py &



#medidas
nohup python /opt/monitorMQTT/MQTT_log.py -c /opt/monitorMQTT/MQTT_log.medidas.config.json -o /opt/monitorMQTT/logs/medidas.log &
#will
nohup python /opt/monitorMQTT/MQTT_log.py -c /opt/monitorMQTT/MQTT_log.will.config.json -o /opt/monitorMQTT/logs/will.log &
#freeheap
nohup python /opt/monitorMQTT/MQTT_log_freeheap.py -c /opt/monitorMQTT/MQTT_log.freeheap.config.json -o /opt/monitorMQTT/logs/freeheap.log &

