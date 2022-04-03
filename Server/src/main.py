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

def main():

    # application variables
    global flap_mode
    flap_mode = False

    # initialization functions
    settings.init()
    commands.init()
    gpio.init()
    motor.init()
    adc.init()
    imu.init()
    elevator.init()
    data_log.init()

    while True:

        # flap mode state
        while flap_mode:
            gpio.BlueLEDBlinker.set_blinking_interval(blink_interval_s=0.5)
            gpio.BlueLEDBlinker.resume() # blink blue LED
            data_log.FileWriter.resume() # start logging data
            motor.LeftMotor.MotorUtils.zero_angle()
            motor.RightMotor.MotorUtils.zero_angle()
            elevator.LeftElevator.ElevatorUtils.zero_angle()
            elevator.RightElevator.ElevatorUtils.zero_angle()
            time.sleep(1)
            motor.LeftMotor.resume()
            motor.RightMotor.resume()
            elevator.LeftElevator.resume()
            elevator.RightElevator.resume()
            while flap_mode:
                pass # hold here until flap mode is deactivated
            motor.LeftMotor.pause() # pause left motor setpoints
            motor.RightMotor.pause() # pause right motor setpoints
            motor.LeftMotor.MotorUtils.stop() # turn off left motor
            motor.RightMotor.MotorUtils.stop() # turn off right motor
            elevator.LeftElevator.pause() # pause left elevator setpoints
            elevator.RightElevator.pause() # pause right elevator setpoints
            elevator.LeftElevator.ElevatorUtils.stop() # turn off left elevator
            elevator.RightElevator.ElevatorUtils.stop() # turn off right elevator
            data_log.FileWriter.pause() # stop logging data 
            gpio.BlueLEDBlinker.pause() # stop blinking blue LED

        # configuration state
        while not flap_mode:
            try:
                s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) # initialize bluetooth socket
                s.bind((settings.SERVER_MAC_ADRRESS, settings.SERVER_PORT))
                s.listen(settings.SERVER_BACKLOG)
                client, _ = s.accept()
                gpio.IOCtrl.turn_on_blue() # turn blue LED on
                while not flap_mode:
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
                        break
                client.close()
                s.close()
            except:
                pass

if __name__=="__main__":
    main()