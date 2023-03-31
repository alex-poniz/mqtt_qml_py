# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QUrl

from AppData import AppData
from AppController import AppController


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    appData = AppData()
    appController = AppController(appData)

    qmlContext = engine.rootContext();
    qmlContext.setContextProperty("appData", appData);
    qmlContext.setContextProperty("appController", appController);

    qml_file = Path(__file__).resolve().parent / "mqtt_qml_gui/main.qml"
    engine.load(qml_file)


    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
