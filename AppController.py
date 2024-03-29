# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject, Property, Signal, Slot
from AppData import AppData
from MqttCommunicator import MqttCommunicator

client_name = "mqtt-qml-paho-test"

class AppController(QObject):
    messageReceived = Signal(str, str)

    def __init__(self, appData):
        QObject.__init__(self)

        self.__appData = appData
        self.__client = MqttCommunicator(client_name)
        self.__client.messageReceived.connect(self.onMessageReceived)
        self.__client.disconnected.connect(self.onDisconnected)

    @Slot(result = bool)
    def connectToBroker(self):
        if (self.__appData.isConnected):
            return False

        self.__client.connectToBroker(self.__appData.hostname, self.__appData.port)
        ret = True
        #ret = m_mqttCommunicator.connect(m_appData.hostname(), m_appData.port());

        self.__appData.isConnected = ret
        return ret

    @Slot()
    def disconnect(self):
        self.__client.disconnect()

    @Slot(str, result = bool)
    def subscribe_sync(self, topic):
        if (not self.__appData.isConnected):
            return False

        ret = self.__client.subscribe(topic)
        #ret = True
        return ret

    @Slot(str, str, result = bool)
    def publish_string(self, topic, message):
        if (not self.__appData.isConnected):
            return False

        ret = self.__client.publish_string(topic, message)
        return ret

    @Slot(str, str)
    def onMessageReceived(self, topic, message):
        print("onMessageReceived: topic: " + topic + " message: " + message)
        self.messageReceived.emit(topic, message)

    @Slot(int)
    def onDisconnected(self, rc):
        self.__appData.isConnected = False
