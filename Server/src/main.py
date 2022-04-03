import socket
import RPi.GPIO as GPIO
import time
import settings
import commands
import gpio
import motor
import adc
import imu
import elevator
import data_log

def check_bluetooth_pair():
    pass

def bluetooth_pair():
    pass

def main():

    # initialize global variables for system state machine
    global bluetooth_paired, flap_mode, bluetooth_pairing_mode
    bluetooth_paired = False
    flap_mode = False
    bluetooth_pairing_mode = False

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

        # check bluetooth pair
        bluetooth_paired = check_bluetooth_pair()
         
        # configuration mode state
        if(bluetooth_paired is True and flap_mode is False and bluetooth_pairing_mode is False):
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # connect bluetooth
            s.bind((settings.SERVER_MAC_ADRRESS, settings.SERVER_PORT))
            s.listen(settings.SERVER_BACKLOG)
            client, _ = s.accept()
            gpio.IOCtrl.turn_on_blue() # turn blue LED on
            while (bluetooth_paired is True and flap_mode is False and bluetooth_pairing_mode is False):
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

        # idle mode state
        if(bluetooth_paired is False and flap_mode is False and bluetooth_pairing_mode is False):
            gpio.IOCtrl.set_blinking_interval(blink_interval_s = 1) # set blinking to 1 second interval (idle mode)
            gpio.BlueLEDBlinker.resume() # blink blue LED 
            while(bluetooth_paired is False and flap_mode is False and bluetooth_pairing_mode is False):
                continue
            gpio.BlueLEDBlinker.pause() # stop blinking blue LED 
        
        # flap mode state
        if(flap_mode is True and bluetooth_pairing_mode is False):
            data_log.FileWriter.resume()
            motor.LeftMotor.MotorUtils.zero_angle()
            motor.RightMotor.MotorUtils.zero_angle()
            time.sleep(1)
            motor.LeftMotor.resume()
            motor.RightMotor.resume()
            while(flap_mode is True and bluetooth_pairing_mode is False):
                continue
            data_log.FileWriter.pause()
            motor.LeftMotor.pause()
            motor.RightMotor.pause()
            motor.LeftMotor.MotorUtils.stop()
            motor.RightMotor.MotorUtils.stop()

        # bluetooth paring state
        if(flap_mode is False and bluetooth_pairing_mode is False):
            bluetooth_pair()
        

if __name__=="__main__":
    main()