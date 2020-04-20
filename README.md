**jatter** is a simple PyQt5 bidirectional Chat Server Example. Using TcpSockets and Server one Server can connect using a GUI Interface (no while loop that is running forever....) to multiple clients.

**Bringup**
```
python server.py
python client.py # Enter name Max
python client.py # Enter name Hans
```
![pyqt5_simple_chatserver](example.png)


**Nice links**
* https://pymotw.com/2/socket/tcp.html


**Tests via Internet**
* Adjust Line 52 in client.py:
```
        HOST = '127.0.0.1' # for online use e.g. from server 192.144.178.26
```
* Adjust Line 47 in server.py:
```
        address = QHostAddress('127.0.0.1') # e.g. use your server ip 192.144.178.26
```
* Use one pc `start server.py`
* use other pc with mobile phone hotspot (not same wlan) `start client.py`
