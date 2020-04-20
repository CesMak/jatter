import sys
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtNetwork import QHostAddress, QTcpServer
import socket

### Copyright
# @Author Markus Lamprecht (www.simact.de), 2020.04.20

# Please start the server first using python server.py

class Server(QDialog):
    def __init__(self):
        super().__init__()

        playbtn = QPushButton('Send', self)
        playbtn.resize(50, 32)
        playbtn.move(10, 10)
        playbtn.clicked.connect(self.send_msg)

        self.label1 = QLabel("");

        self.label = QLabel("Received Messages from Clients appear here");
        self.label.setWordWrap(1);

        self.textbox = QLineEdit(self)
        self.textbox.move(10, 50)
        self.textbox.resize(600, 32)
        self.setWindowTitle("Server")
        self.resize(600,300)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(playbtn)
        self.setLayout(layout)

        self.tcpServer   = None
        self.clientConnections= []
        self.blockSize = 0
        self.getIP()

    def sessionOpened(self):
        self.tcpServer = QTcpServer(self)
        PORT = 8000
        address = QHostAddress('127.0.0.1') # e.g. use your server ip 192.144.178.26
        if not self.tcpServer.listen(address, PORT):
            print("cant listen!")
            self.close()
            return
        self.tcpServer.newConnection.connect(self.serverInputCommunication)

    def send_msg(self):
        block = QByteArray()
        # QDataStream class provides serialization of binary data to a QIODevice
        out = QDataStream(block, QIODevice.ReadWrite)
        # We are using PyQt5 so set the QDataStream version accordingly.
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)
        text_box_msg = self.textbox.text()
        to =""
        msg =""
        if "@" not in text_box_msg:
            print("TO whom should I send a message? use e.g. @all Hello all or @Max Hello max")
            return
        else:
            to, msg =text_box_msg.split(' ', 1)[0], text_box_msg.split(' ', 1)[1]
            to = to.replace("@", "")

        # get a byte array of the message encoded appropriately.
        message = bytes(msg, encoding='ascii')
        # now use the QDataStream and write the byte array to it.
        out.writeString(message)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        aaa = True
        if to=="all":
            for conn in self.clientConnections:
                conn["conn"].write(block)
        else:
            for conn in self.clientConnections:
                if conn["name"] == to:
                    conn["conn"].write(block)
                    aaa = False
        if aaa:
            print("Sry I server could not send message to", to)

    def cl1Input(self):
        for conn in self.clientConnections:
            #conn.waitForReadyRead()
            # read incomming data
            instr = conn["conn"].readAll()
            # in this case we print to the terminal could update text of a widget if we wanted.
            in_msg = str(instr, encoding='ascii')
            try:
                name, message = in_msg.split(",")[0], in_msg.split(",")[1]
                if not "name" in conn:
                    conn["name"] = name
            except:
                print(in_msg, conn["idx"])
                name = None
            if name is not None:
                self.label.setText(self.label.text()+"\n"+name+"\t"+message)

    def getIP(self):
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        print(ip_address, hostname)
        self.label1.setText(hostname+" "+str(ip_address))
        return ip_address, hostname

    def serverInputCommunication(self):
        print("serverInputCommunication")
        self.clientConnections.append({"conn":self.tcpServer.nextPendingConnection(), "idx": len(self.clientConnections)})
        self.clientConnections[len(self.clientConnections)-1]["conn"].readyRead.connect(self.cl1Input)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.sessionOpened()
    sys.exit(server.exec_())


# import socket
# from _thread import *
# import sys
#
# # Global variables:
# server        = ip_address
# port          = 5555
# players       = [] # type: {"name": "", "idx": 0}
# max_players   = 2
#
# hostname = socket.gethostname()
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# ip_address = s.getsockname()[0]
#
# ## printing the hostname and ip_address
# print(f"Hostname: {hostname}")
# print(f"IP Address: {ip_address}")
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)
#
# s.listen(2)
# print("Waiting for a connection, Server Started")
#
# def threaded_client(conn, player_idx):
#     conn.send(str.encode("Server sends: Hey new Player ", player_idx, "What is your name?"))
#     reply = "Server sends: Game is starting now"
#     while True:
#         try:
#             data = conn.recv(2048).decode()
#             if not data:
#                 print("Disconnected")
#                 break
#             else:
#                 print("Received: ", data)
#                 print("Sending : ", reply)
#
#             conn.sendall(str.encode(make_pos(reply)))
#         except:
#             break
#
#     print("Lost connection")
#     conn.close()
#
# while True:
#     conn, addr = s.accept()
#     print("Server is connected to:", addr)
#     start_new_thread(threaded_client, (conn, len(players)))
