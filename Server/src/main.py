import socket
import RPi.GPIO as GPIO
import settings
import commands
import gpio
import motor
import adc

def main():

    # gpio settings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    settings.init()
    commands.init()
    gpio.init()
    motor.init()
    adc.init()

    while True:
        s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.bind((settings.SERVER_MAC_ADRRESS, settings.SERVER_PORT))
        s.listen(settings.SERVER_BACKLOG)
        client, _ = s.accept()
        while True:
            try:
                recv_str = client.recv(settings.BUFFER_SIZE).decode().upper()
                if recv_str:
                    recv_str_list = recv_str.split()
                    command = recv_str_list[0]
                    if command in commands.command_dict.keys():
                        try:
                            args = recv_str_list[1:]
                        except IndexError:
                            args = []
                        return_str = commands.command_dict[command](args)
                        client.send(return_str.encode())
                    else:
                        client.send('Invalid Command!'.encode())
            except ConnectionResetError:
                client.close()
                s.close()
                break

if __name__=="__main__":
    main()