import socket
import settings
import commands
import MotorDriver

def main():

    settings.init()
    commands.init()
    MotorDriver.init()

    while True:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.bind((settings.serverMACAddress, settings.serverPort))
        s.listen(settings.serverBacklog)
        client, _ = s.accept()
        while True:
            try:
                recvStr = client.recv(settings.bufferSize).decode().upper()
                if recvStr:
                    recvStrList = recvStr.split()
                    command = recvStrList[0]
                    if command in commands.commandDict.keys():
                        try:
                            args = recvStrList[1:]
                        except IndexError:
                            args = []
                        returnStr = commands.commandDict[command](args)
                        client.send(returnStr.encode())
                    else:
                        client.send('Invalid Command!'.encode())
            except ConnectionResetError:
                client.close()
                s.close()
                break

if __name__=="__main__":
    main()