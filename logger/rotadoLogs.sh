#!/bin/bash

#medidas
rm -rf /opt/monitorMQTT/logs/medidas.log.sav
mv /opt/monitorMQTT/logs/medidas.log /opt/monitorMQTT/logs/medidas.log.sav

#will
rm -rf /opt/monitorMQTT/logs/will.log.sav
mv /opt/monitorMQTT/logs/will.log /opt/monitorMQTT/logs/will.log.sav

#freeheap
rm -rf /opt/monitorMQTT/logs/freeheap.log.sav
mv /opt/monitorMQTT/logs/freeheap.log /opt/monitorMQTT/logs/freeheap.log.sav

#salida
rm -rf /opt/monitorMQTT/logs/salida.log.sav
mv /opt/monitorMQTT/logs/salida.log /opt/monitorMQTT/logs/salida.log.sav


