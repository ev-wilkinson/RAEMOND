import socket

serverMACAddress = 'B8:27:EB:C3:F3:BC' # MAC address of server (raspberry pi)
serverPort = 2 # arbitrary but has to match server
bufferSize = 1024 # buffer size
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, serverPort))

while True:
    s.send(input().encode())
    while True:
        data = s.recv(bufferSize)
        if data:
            print(data.decode())
            break
s.close()