import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15

Dialog {
    id: brokerDialogID
    signal dialogAccepted()
    //property alias text : textContainer.text


    standardButtons: DialogButtonBox.Ok
    modal: true

    RowLayout {
        Text {
            text: "Host: "
        }

        TextField {
            id: hostEdit

            text: appData.hostname
            focus: true
            }

        Text {
            text: "Port: "
        }

        TextField {
            id: portEdit

            text: appData.port
            focus: true
        }
    }

    onAccepted: {
        appData.hostname = hostEdit.text
        appData.port = portEdit.text

        // emit signal dialogAccepted()
        dialogAccepted();
    }
}
