import socket
import RPi.GPIO as GPIO
import settings
import commands
import gpio
import motor
import adc
import imu
import elevator
import data_log

def main():

    # gpio settings
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    settings.init()
    commands.init()
    gpio.init()
    motor.init()
    adc.init()
    imu.init()
    elevator.init()
    data_log.init()

    while True:

        # state with button enabled
        while gpio.button_enabled:
            gpio.IOCtrl.turn_off_blue() # turn off blue LED 
            print('Motors running...')

        # state with button disabled
        while not gpio.button_enabled:
            if gpio.BlueLEDBlinker.paused:
                gpio.BlueLEDBlinker.resume() # blink blue LED    
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # connect bluetooth
            s.bind((settings.SERVER_MAC_ADRRESS, settings.SERVER_PORT))
            s.listen(settings.SERVER_BACKLOG)
            client, _ = s.accept()
            gpio.BlueLEDBlinker.pause() # stop blinking blue LED  
            gpio.IOCtrl.turn_on_blue() # keep blue LED on
            while not gpio.button_enabled:
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