# This Python file uses the following encoding: utf-8

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
#QML_IMPORT_NAME = "io.qt.app_properties"
#QML_IMPORT_MAJOR_VERSION = 1

from PySide6.QtCore import QObject, Property, Signal, Slot

class AppData(QObject):

    portChanged = Signal(int)
    hostnameChanged = Signal(str)
    isConnectedChanged = Signal(bool)

    def __init__(self):
        QObject.__init__(self)

        self.__port = 1883;
        self.__hostname = ""
        self.__isConnected = False;

    #@Slot(result = int)
    def getPort(self):
        return self.__port

    #@Slot(int)
    def setPort(self, portParam):
        if self.__port == portParam:
            return

        self.__port = portParam
        self.hostnameChanged.emit(self.__port)

    def getHostname(self):
        return self.__hostname

    def setHostname(self, hostnameParam):
        if self.__hostname == hostnameParam:
            return

        self.__hostname = hostnameParam
        self.hostnameChanged.emit(self.__hostname)

    def getIsConnected(self):
        return self.__isConnected

    def setIsConnected(self, isConnectedParam):
        if self.__isConnected == isConnectedParam:
            return

        self.__isConnected = isConnectedParam
        self.isConnectedChanged.emit(self.__isConnected)


    port = Property(int, getPort, setPort, notify=portChanged)
    hostname = Property(str, getHostname, setHostname, notify=hostnameChanged)
    isConnected = Property(bool, getIsConnected, setIsConnected, notify=isConnectedChanged)

