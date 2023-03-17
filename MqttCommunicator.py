# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Property, Signal, Slot
from paho.mqtt import client as mqtt_client

import _thread


def threadFunc(client):
    print("Starting MQTT loop thread")
    client.loop_forever()


class MqttCommunicator(QObject):
    connected = Signal(int)
    disconnected = Signal(int)
    messageReceived = Signal(str, str)

    def __init__(self, client_id):
        QObject.__init__(self)

        self.__client = mqtt_client.Client(client_id)
        self.__client.on_log = self.onLog
        self.__client.on_connect = self.onConnect
        self.__client.on_disconnect = self.onDisconnect
        self.__client.on_subscribe = self.onSubscribe
        self.__client.on_message = self.onMessage
        #client.username_pw_set(username, password)


    def startMqttLoop(self):
        _thread.start_new_thread(threadFunc, (self.__client, ))

    def onLog(self, client, userdata, level, buf):
        print("log message: ", buf)

    def onSubscribe(self, client, userdata, mid, granted_qos):
        print("Called onSubscribe()")

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

        self.connected.emit(rc)

    def onDisconnect(self, client, userdata, rc):
        print("Called onDisconnect()")
        if (rc != mqtt_client.MQTT_ERR_SUCCESS):
            print("Unexpected disconnection!!!")

        self.disconnected.emit(rc)

    def onMessage(self, client, userdata, message):
        encoding = 'utf-8'
        strMessage = message.payload.decode(encoding)
        print("Received message '" + strMessage + "' on topic '" + message.topic)
        self.messageReceived.emit(message.topic, strMessage)


    def connectToBroker(self, hostname, port):
        self.__client.connect(hostname, port)
        self.startMqttLoop()

    def disconnect(self):
        self.__client.disconnect()

    def subscribe(self, topic):
        ret = self.__client.subscribe(topic)

        return ret[0] == mqtt_client.MQTT_ERR_SUCCESS

    def publish_string(self, topic, message):
        messageInfo = self.__client.publish(topic, message)

        return messageInfo.rc == mqtt_client.MQTT_ERR_SUCCESS




