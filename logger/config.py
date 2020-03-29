import json

OK                          =  0
CONFIGURACION_POR_DEFECTO   = -1
ERROR_FICHERO_CONFIGURACION = -2
INICIAL                     = -100

class Configuracion:
    __Broker_IP = 0
    __Broker_Puerto = 0
    __sub_topic = 0
    __pub_topic =0
    __DB_IP = 0
    __DB_Puerto = 0
    __BaseDatos = 0
    __Measurement =0
    __configurado = INICIAL

    def __init__(self, fichero, debug = False, Broker_IP = "0.0.0.0",Broker_Puerto = "0",sub_topic = '',pub_topic = '',DB_IP = "0.0.0.0",DB_Puerto = 0,BaseDatos = '',Measurement = ''):
        #valores por defecto sobre el bus MQTT
        __Broker_IP = Broker_IP
        __Broker_Puerto = Broker_Puerto
        __sub_topic = sub_topic
        __pub_topic = pub_topic

        #valores por defecto sobre la base de datos InfluxDB
        __DB_IP = DB_IP
        __DB_Puerto = DB_Puerto
        __BaseDatos = BaseDatos
        __Measurement = Measurement

        self.__leeConfiguracion(fichero,debug)

    def __leeConfiguracion(self,fichero,debug=False):
        if (debug==True): print("\nInicio de configuracion----------------------------------------------------------------------")
        self.__configurado = OK #por defecto va bien...

        try:
            #leo el fichero de configuracion
            with open(fichero) as json_file:
                configuracion = json.load(json_file)
                if (debug==True): print("Configuracion leida=\n %s" %configuracion)
        except :
            if (debug==True): print("No se pudo obtener el fichero de configuracion")
            self.__configurado = ERROR_FICHERO_CONFIGURACION
            return

        if configuracion.has_key('MQTT'): 
            MQTTConfig = configuracion['MQTT']

            if MQTTConfig.has_key('Broker_IP'): self.setBroker_IP(MQTTConfig.pop("Broker_IP"))
            else: 
                if (debug==True): 
                    print("Broker_IP no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if MQTTConfig.has_key('Broker_Puerto'): self.setBroker_Puerto(MQTTConfig.pop("Broker_Puerto"))
            else: 
                if (debug==True): 
                    print("Broker_Puerto no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if MQTTConfig.has_key('sub_topic'): self.setsub_topic(MQTTConfig.pop("sub_topic"))
            else: 
                if (debug==True): 
                    print("sub_topic no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if MQTTConfig.has_key('pub_topic'): self.setpub_topic(MQTTConfig.pop("pub_topic"))
            else: 
                if (debug==True): 
                    print("pub_topic no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO
        else: 
            if (debug==True): 
                print("No se ha configurado MQTT. Valores pore defecto")
                self.__configurado = CONFIGURACION_POR_DEFECTO

        if configuracion.has_key('DB'): 
            DBConfig = dict(configuracion['DB'])

            if DBConfig.has_key('DB_IP'): self.setDB_IP(DBConfig.pop("DB_IP"))
            else: 
                if (debug==True): 
                    print("DB_IP no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if DBConfig.has_key('DB_Puerto'): self.setDB_Puerto(DBConfig.pop("DB_Puerto"))
            else: 
                if (debug==True): 
                    print("DB_Puerto no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if DBConfig.has_key('BaseDatos'): self.setBaseDatos(DBConfig.pop("BaseDatos"))
            else: 
                if (debug==True): 
                    print("BaseDatos no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO

            if DBConfig.has_key('Measurement'): self.setMeasurement(DBConfig.pop("Measurement"))
            else: 
                if (debug==True): 
                    print("Measurement no esta configurado. Valor por defecto.")
                    self.__configurado = CONFIGURACION_POR_DEFECTO
        else:
            if (debug==True): 
                print("No se ha configurado DB. Valores pore defecto")
                self.__configurado = CONFIGURACION_POR_DEFECTO

        if (debug==True): print("Configuracion de MQTT")
        if (debug==True): print("Broker_IP = %s" %self.__Broker_IP)
        if (debug==True): print("Broker_Puerto = %s" %self.__Broker_Puerto)
        if (debug==True): print("sub_topic = %s" %self.__sub_topic)
        if (debug==True): print("pub_topic = %s" %self.__pub_topic)

        if (debug==True): print("Configuracion de DB Influx")
        if (debug==True): print("DB_IP = %s" %self.__DB_IP)
        if (debug==True): print("DB_Puerto = %s" %self.__DB_Puerto)
        if (debug==True): print("BaseDatos = %s" %self.__BaseDatos)
        if (debug==True): print("Measurement = %s" %self.__Measurement)


    def setBroker_IP(self,valor): self.__Broker_IP=valor
    def setBroker_Puerto(self,valor): self.__Broker_Puerto=valor
    def setsub_topic(self,valor): self.__sub_topic=valor
    def setpub_topic(self,valor): self.__pub_topic=valor
    def setDB_IP(self,valor): self.__DB_IP=valor
    def setDB_Puerto(self,valor): self.__DB_Puerto=valor
    def setBaseDatos(self,valor): self.__BaseDatos=valor
    def setMeasurement(self,valor): self.__Measurement=valor

    def getBroker_IP(self): return self.__Broker_IP
    def getBroker_Puerto(self): return self.__Broker_Puerto
    def getsub_topic(self): return self.__sub_topic
    def getpub_topic(self): return self.__pub_topic
    def getDB_IP(self): return self.__DB_IP
    def getDB_Puerto(self): return self.__DB_Puerto
    def getBaseDatos(self): return self.__BaseDatos
    def getMeasurement(self): return self.__Measurement

    def getConfigurado(self): return self.__configurado

#c=Configuracion('MQTT_log.config.json',True)
#print("la salida es %i\n" %c.getConfigurado())