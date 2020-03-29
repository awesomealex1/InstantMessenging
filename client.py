from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from Designs.design1 import Ui_MainWindow
import sys


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.send)

        self.HOST = "127.0.0.1"
        if self.HOST == "":
            self.HOST = "127.0.0.1"

        self.PORT = 32000
        if not self.PORT:
            self.PORT = 32000
        else:
            self.PORT = int(self.PORT)

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                prev_text = self.ui.label.text()
                self.ui.label.setText(prev_text + "\n" + msg)
            except OSError:  # Possibly client has left the chat.
                break

    def send(self):
        #self.ui.label.setText("Hello")
        msg = self.ui.textEdit.toPlainText()
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()