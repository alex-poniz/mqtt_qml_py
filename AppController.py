# This Python file uses the following encoding: utf-8

from PySide6.QtCore import QObject, Property, Signal, Slot
from AppData import AppData

class AppController(QObject):
    def __init__(self, appData):
        QObject.__init__(self)

        self.__appData = appData

    @Slot(result = bool)
    def connectToBroker(self):
        if (self.__appData.isConnected):
            return False

        ret = True
        #ret = m_mqttCommunicator.connect(m_appData.hostname(), m_appData.port());

        self.__appData.isConnected = ret
        return ret

    @Slot(str, result = bool)
    def subscribe_sync(self, topic):
        if (self.__appData.isConnected):
            return False

        ret = True
        return ret

    @Slot(str, str, result = bool)
    def publish_string(self, topic, message):
        if (self.__appData.isConnected):
            return False

        ret = True
        return ret



    #        void onMessageReceived(const QString& topic, const QString& message);
    #        bool onInputTextChanged(const QString& topic, const QString& message);
