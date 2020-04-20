from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

### Copyright
# @Author Markus Lamprecht (www.simact.de), 2020.04.20


class Client(QDialog):
    def __init__(self):
        super().__init__()
        playbtn = QPushButton('Send', self)
        playbtn.resize(50, 32)
        playbtn.move(10, 10)
        playbtn.clicked.connect(self.send_msg)

        self.label = QLabel("Received Messages from Server appear here");
        self.label.setWordWrap(1);

        self.textbox = QLineEdit(self)
        self.textbox.move(10, 50)
        self.textbox.resize(50, 32)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(playbtn)
        self.setLayout(layout)

        self.resize(600,100)


        print('Enter your name:')
        self.name = input()
        self.setWindowTitle("Client "+self.name)
        self.tcpSocket = QTcpSocket(self)
        self.blockSize = 0
        self.makeRequest()
        self.tcpSocket.readyRead.connect(self.dealCommunication)
        self.tcpSocket.error.connect(self.displayError)

        # send start message:
        self.tcpSocket.waitForConnected(1000)
        self.tcpSocket.write(bytes( self.name+","+"Server please init me with my name", encoding='ascii'))

    def send_msg(self):
        print("inside send_msg")
        self.tcpSocket.waitForConnected(1000)
        self.tcpSocket.write(bytes( self.name+","+self.textbox.text(), encoding='ascii'))

    def makeRequest(self):
        HOST = '127.0.0.1'
        PORT = 8000
        self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)

    def dealCommunication(self):
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        #print(instr, self.blockSize, self.tcpSocket.bytesAvailable())
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            self.blockSize = instr.readUInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
        # Print response to terminal, we could use it anywhere else we wanted.
        self.label.setText(self.label.text()+"\n"+str(instr.readString(), encoding='ascii'))
        self.blockSize = 0

    def displayError(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            pass
        else:
            print(self, "The following error occurred: %s." % self.tcpSocket.errorString())


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    client = Client()
    sys.exit(client.exec_())





# from PyQt5.QtCore import QDataStream, QIODevice
# from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
# from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket
#
# class Client(QDialog):
#     def __init__(self):
#         super().__init__()
#         playbtn = QPushButton('Send', self)
#         playbtn.resize(50, 32)
#         playbtn.move(10, 10)
#         playbtn.clicked.connect(self.send_msg)
#
#     def send_msg(self):
#         print("inside send_msg")
#         self.tcpSocket = QTcpSocket(self)
#         self.blockSize = 0
#         self.makeRequest()
#         self.tcpSocket.waitForConnected(1000)
#         # send any message you like it could come from a widget text.
#         self.tcpSocket.write(b'Max,InitPlayer,me')
#         self.tcpSocket.readyRead.connect(self.dealCommunication)
#         self.tcpSocket.error.connect(self.displayError)
#
#     def makeRequest(self):
#         HOST = '127.0.0.1'
#         PORT = 8000
#         self.tcpSocket.connectToHost(HOST, PORT, QIODevice.ReadWrite)
#
#     def dealCommunication(self):
#         print("inside client dealCommunication")
#         instr = QDataStream(self.tcpSocket)
#         instr.setVersion(QDataStream.Qt_5_0)
#         print(instr, self.blockSize, self.tcpSocket.bytesAvailable())
#         if self.blockSize == 0:
#             if self.tcpSocket.bytesAvailable() < 2:
#                 return
#             self.blockSize = instr.readUInt16()
#         # if self.tcpSocket.bytesAvailable() < self.blockSize:
#         #     return
#         # Print response to terminal, we could use it anywhere else we wanted.
#         print(str(instr.readString(), encoding='ascii'))
#
#     def displayError(self, socketError):
#         if socketError == QAbstractSocket.RemoteHostClosedError:
#             pass
#         else:
#             print(self, "The following error occurred: %s." % self.tcpSocket.errorString())
#
#
# if __name__ == '__main__':
#     import sys
#
#     app = QApplication(sys.argv)
#     client = Client()
#     sys.exit(client.exec_())
#



# import socket
#
#
# class Network:
#     def __init__(self, name):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server = self.getIP() ##"YOUR LOCAL IPV4"
#         self.port   = 5555
#         print(self.server, self.port)
#         self.addr   = (self.server, self.port)
#         self.msg    = self.connect()
#         self.name   = name
#
#     def parse(self):
#         print("I received", self.msg)
#         unique, msg = self.msg.split(",")[0], self.msg.split(",")[1]
#         if unique =="INIT_PLAYER" or unique == "WAIT_FOR_OTHERS":
#             return "Name"+","+"Max"
#         if unique =="ALL_CONNECTED":
#             if msg==self.name:
#                 return "Play"+","+"0" #<<<last is hand card index
#             else:
#                 return "Not_my_turn"+","+self.name
#         else:
#             return "NO_IDEA_WHAT_TO_SEND"+","+" "
#
#     def getIP(self):
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(("8.8.8.8", 80))
#         return s.getsockname()[0]
#
#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(2048).decode()
#         except Exception as e:
#             print(e)
#             pass
#
#     def send(self, data):
#         try:
#             self.client.send(str.encode(data))
#             return self.client.recv(2048).decode()
#         except socket.error as e:
#             print(e)
#
# n = Network("Max")
# while True:
#     reply = n.parse()
#     replyy = n.send(reply)
#     if replyy is not None:
#         n.msg = replyy
