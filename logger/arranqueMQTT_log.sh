#! /bin/sh

#Los comando funcionan en la consola pero no aqui, la consola no es sh

#medidas
nohup python /opt/monitorMQTT/MQTT_log.py -c /opt/monitorMQTT/MQTT_log.medidas.config.json -o /opt/monitorMQTT/logs/medidas.log &
#will
nohup python /opt/monitorMQTT/MQTT_log.py -c /opt/monitorMQTT/MQTT_log.will.config.json -o /opt/monitorMQTT/logs/will.log &
