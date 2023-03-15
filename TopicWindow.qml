import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

    Window {
        property int index : 0
        property string outputText

        id: topicWindow
        width: 400
        height: 300

        ColumnLayout{
            spacing: 2
            Layout.fillWidth: true
            width: parent.width
            height: parent.height

            TextArea {
                id: input
                //Layout.alignment: Qt.AlignCenter
                Layout.preferredHeight: 100
                Layout.fillWidth: true
                width: parent.width
                wrapMode: TextEdit.Wrap
                focus: true
                background: Rectangle {
                    border.color: "black"
                }
                onTextChanged: {
                    var fullLength = text.length;
                    if (fullLength > 1 && text.endsWith('\n')) {
                        var prevCRIndex = text.lastIndexOf('\n', fullLength - 2);
                        var message = text.substring(prevCRIndex + 1, fullLength - 1);
                        console.log("Sending message '" + message + "' to topic " + topicWindow.title);
                        appController.publish_string(topicWindow.title, message);
                    }
                }
            }

            TextArea {
                id: output
                Layout.fillWidth: true
                Layout.fillHeight: true
                width: parent.width
                readOnly: true
                wrapMode: TextEdit.Wrap
                textFormat: "RichText"
                text: outputText

                focus: false

                background: Rectangle {
                    border.color: "black"
                }
            }
        }
    }

