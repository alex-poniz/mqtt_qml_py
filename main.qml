import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15


ApplicationWindow {
    id: mainWindow
    width: 600
    height: 120
    visible: true
    title: qsTr("MQTTBrowser")

    property list<Window> windowsList

    Connections{
        target: appController
        function onMessageReceived(topic, message) {
            var index = appData.getIndexByTopic(topic)
            var win = windowsList[index];
            win.outputText += "<BR>" + message
        }
    }

    function publishMessage() {
        if (appController.publish_string(topicTextField.text, messageTextField.text)) {
            topicTextField.clear()
            messageTextField.clear()
        }
    }

    function disconnect() {
        appController.disconnect()
    }

    function showBrokerDialog() {
        var component = Qt.createComponent("BrokerDialog.qml")
        if (component.status === Component.Ready) {
            var dialog = component.createObject(mainWindow)

            dialog.title = qsTr("MQTT broker");
            dialog.dialogAccepted.connect(brokerDialogClosed)

            dialog.open()
        } else
            console.error(component.errorString())
    }

    function brokerDialogClosed()
    {
        appController.connectToBroker();
    }

    function showTopicDialog() {
        var component = Qt.createComponent("TopicDialog.qml")
        if (component.status === Component.Ready) {
            var dialog = component.createObject(mainWindow)

            dialog.title = qsTr("MQTT topic");
            dialog.dialogAccepted.connect(topicDialogClosed)

            dialog.open()
        } else
            console.error(component.errorString())
    }

    function topicDialogClosed(topicname)
    {
        if (appController.subscribe_sync(topicname)) {
            var component = Qt.createComponent("TopicWindow.qml")
            if (component.status === Component.Ready) {
                var win = component.createObject(mainWindow)

                win.title = topicname;
                win.x = win.x + windowsList.length * 20;
                win.y = win.y + windowsList.length * 20;
                win.index = windowsList.length;
                windowsList.push(win);
                appData.addTopic(topicname);

                win.show();
            } else
                console.error(component.errorString())
        }
        console.log("topicDialogClosed: end")
    }

    menuBar: MenuBar {
           Menu {
               title: qsTr("&File")
               Action {
                   text: qsTr("&Connect...")
                   onTriggered: showBrokerDialog();
                   enabled: !appData.isConnected
               }

               Action {
                   text: qsTr("&Disconnect")
                   onTriggered: disconnect();
                   enabled: appData.isConnected
               }

               Action {
                   text: qsTr("&Subscribe...")
                   onTriggered: showTopicDialog();
                   enabled: appData.isConnected
               }
               MenuSeparator { }
               Action {
                   text: qsTr("&Quit")
                   onTriggered: mainWindow.close()
               }
           }
           Menu {
               title: qsTr("&Help")
               Action { text: qsTr("&About") }
           }
       }

    RowLayout {
        x: 10
        y: 20
        spacing: 10
        width:  mainWindow.width - 2*10

        Text {
            text: "MQTT topic: "
        }

        TextField {
            id: topicTextField
            enabled: appData.isConnected
        }

        Text {
            text: "Message: "
        }

        TextField {
            id: messageTextField
            enabled: appData.isConnected
            Layout.fillWidth: true
            onAccepted: publishMessage()
        }

        Button {
            text: "Publish"
            enabled: appData.isConnected
            onClicked: publishMessage()
        }
    }

    Rectangle {
        id: statusBar
        y: parent.height - height
        width:  mainWindow.width
        height: 25
        border.color: "black"

        RowLayout {
            x: 10
            spacing: 10
            width: mainWindow.width - 2*10
            anchors.margins: 5

            Text {
                text: "MQTT broker: "
            }

            Text {
                id: hostnameText
                text: appData.hostname
            }

            Rectangle {
                Layout.fillWidth: true;
            }

            Text {
                text: "Connection status: "
            }

            Rectangle {
                id: connectionStatus
                y: 10
                width: 15
                height: 15
                radius: 7

                color: appData.isConnected ? "green" : "red"
            }
        }
    }
}
