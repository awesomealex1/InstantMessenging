from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from Designs.design3 import Ui_MainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtCore
import sys


class ApplicationWindow(QtWidgets.QMainWindow):

    trigger = pyqtSignal(str)

    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send)
        self.ui.textEdit.installEventFilter(self)
        self.HOST = "127.0.0.1"
        if self.HOST == "":
            self.HOST = "127.0.0.1"

        self.PORT = 32000
        if not self.PORT:
            self.PORT = 32000
        else:
            self.PORT = int(self.PORT)

        self.trigger.connect(self.add_msg)

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def add_msg(self, msg):
        prev_text = self.ui.textEdit_2.toPlainText()
        if prev_text != "":
            self.ui.textEdit_2.setText(prev_text + "\n" + msg)
        else:
            self.ui.textEdit_2.setText(msg)
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.trigger.emit(msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self):
        msg = self.ui.textEdit.toPlainText()
        self.client_socket.send(bytes(msg, "utf8"))
        self.ui.textEdit.setText("")
    
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.ui.textEdit:
            if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and self.ui.textEdit.hasFocus():
                self.send()
                return True
        return False

    def close_sockets(self):
        self.client_socket.close()

    def closeEvent(self, event):
        self.close_sockets()

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())
    application.close_sockets()

if __name__ == "__main__":
    main()