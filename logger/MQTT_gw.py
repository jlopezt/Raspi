import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

BrokerOrigen = "10.68.1.100"
BrokerDestino = "10.68.2.101"

sub_topic = "casa/#"    # receive messages on this topic


# mqtt section

# when connecting to mqtt do this;

def on_connect(client, userdata, flags, rc):
    print("Conectado con el codigo de resultado "+str(rc))
    client.subscribe(sub_topic)

# when receiving a mqtt message do this;

def on_message(client, userdata, msg):
#    message = str(msg.payload)
#    print(msg.topic+" "+message)
    clienteHabla.publish(msg.topic,msg.payload)

#def on_publish(mosq, obj, mid):
#    print("mid: " + str(mid))


clienteHabla = mqtt.Client()
clienteHabla.username_pw_set("domoticae", "88716")
clienteHabla.connect(BrokerDestino, 1883, 60)


clienteEscucha = mqtt.Client()
clienteEscucha.on_connect = on_connect
clienteEscucha.on_message = on_message

clienteEscucha.username_pw_set("domoticae", "88716")
clienteEscucha.connect(BrokerOrigen, 1883, 60)
clienteEscucha.loop_forever()


