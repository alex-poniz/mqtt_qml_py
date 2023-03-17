import QtQuick 2.15
import QtQuick.Controls 2.15

Dialog {
    id: topicDialogID
    signal dialogAccepted(string text)

    standardButtons: DialogButtonBox.Ok
    modal: true

    TextField {
        id: textContainer
        focus: true
        onAccepted: {
            dialogAccepted(textContainer.text)
            topicDialogID.close()
        }
    }

    onAccepted: {
        // emit signal dialogAccepted()
        dialogAccepted(textContainer.text)
    }
}
