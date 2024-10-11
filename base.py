from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from speech_recognizer import recog_me


def main():
    app = QApplication([])
    window= QWidget()
    window.setGeometry(100, 100, 400, 300)
    window.setWindowTitle("My Chatbot")

     
    layout = QVBoxLayout()

    label = QLabel("Press the button below")
    textbox= QTextEdit()
    button= QPushButton("Press Me!")

    button.clicked.connect(lambda: on_click(textbox.toPlainText()))
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)
    # label = QLabel(window)
    # label.setText("Press the button below!")
    # label.setFont(QFont("Arial", 16))
    # label.move(50,100)

    window.setLayout(layout)
    window.show()
    app.exec_()

def on_click(msg):
    message= QMessageBox()
    message.setText(msg)
    message.exec_()
if __name__== '__main__':
    main()

