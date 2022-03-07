import socket
from MotorDriver import *

def motor_config(args):
    try:
        if args[0] == 'SHOW':
            return 'Under Development!'

        elif args[0] == 'ZERO':
            if args[1] == 'LEFT':
                LMotor.pause()
                return LMotor.motorUtils.zeroMotor()
            elif args[1] == 'RIGHT':
                RMotor.pause()
                return RMotor.motorUtils.zeroMotor()
            elif args[1] == 'BOTH':
                LMotor.pause()
                RMotor.pause()
                return f'LEFT: {LMotor.motorUtils.zeroMotor()}\nRIGHT: {RMotor.motorUtils.zeroMotor()}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ANGLE':
            if args[1] == 'LEFT':
                LMotor.pause()
                return LMotor.motorUtils.setAngleDeg(float(args[2]))
            elif args[1] == 'RIGHT':
                RMotor.pause()
                return RMotor.motorUtils.setAngleDeg(float(args[2]))
            elif args[1] == 'BOTH':
                LMotor.pause()
                RMotor.pause()
                return f'LEFT: {LMotor.motorUtils.setAngleDeg(float(args[2]))}\nRIGHT: {RMotor.motorUtils.setAngleDeg(float(args[2]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'SET':

            if args[2] == 'FREQ':
                if args[1] == 'LEFT':
                    return LMotor.motorUtils.setFlapFreqHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.motorUtils.setFlapFreqHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.motorUtils.setFlapFreqHz(float(args[3]))}\nRIGHT: {RMotor.motorUtils.setFlapFreqHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'AMP':
                if args[1] == 'LEFT':
                    return LMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))}\nRIGHT: {RMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'SRATE':
                if args[1] == 'LEFT':
                    return LMotor.motorUtils.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.motorUtils.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.motorUtils.setFlapSampleRateHz(float(args[3]))}\nRIGHT: {RMotor.motorUtils.setFlapSampleRateHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'
            
            elif args[2] == 'DELAY':
                return 'Under Development!'

            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                try:
                    LMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'RIGHT':
                try:
                    RMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'BOTH':
                try:
                    LMotor.resume()
                    RMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                LMotor.pause()
                return LMotor.motorUtils.stopMotor()
            elif args[1] == 'RIGHT':
                RMotor.pause()
                return RMotor.motorUtils.stopMotor()
            elif args[1] == 'BOTH':
                LMotor.pause()
                RMotor.pause()
                return f'LEFT: {LMotor.motorUtils.stopMotor()}\nRIGHT: {RMotor.motorUtils.stopMotor()}'
            else:
                return 'Invalid Command Arguments!'
        
        else:
            return 'Invalid Command Arguments!'

    except IndexError:
        return 'Invalid Command Arguments!'

def adc_config(args):
    return 'Under Development!'

def imu_config(args):
    return 'Under Development!'

def elevator_config(args):
    return 'Under Development!'

def terminate_program(args):
    return 'Under Development!'

def print_help(args):
    return ('\nCommands:\n'
            'HELP\n'                                     
            'TERMINATE\n'                                
            'MOTOR SHOW [LEFT|RIGHT|BOTH]\n'             
            'MOTOR ZERO [LEFT|RIGHT|BOTH]\n'             
            'MOTOR ANGLE [LEFT|RIGHT|BOTH] [value]\n'
            'MOTOR SET [LEFT|RIGHT|BOTH] [FREQ|AMP|SRATE|DELAY] [value]\n'
            'MOTOR START [LEFT|RIGHT|BOTH]\n'    
            'MOTOR STOP [LEFT|RIGHT|BOTH]\n'             
            'ADC SHOW\n'                                 
            'IMU SHOW\n'                                 
            'ELEVATOR SET [value]\n'                     
            'ELEVATOR SHOW\n'                            
    )

commandDict = {'HELP': print_help,
               'MOTOR': motor_config,
               'ADC': adc_config,
               'IMU': imu_config,
               'ELEVATOR': elevator_config,
               'TERMINATE': terminate_program
}

RMotor = Motor(pwm_channel=0)
RMotor.start()
LMotor = Motor(pwm_channel=1)
LMotor.start()

serverMACAddress = 'B8:27:EB:C3:F3:BC' # MAC address of server (raspberry pi)
serverPort = 2 # arbitrary but has to match client
serverBacklog = 1 # specifies number of unaccepted connections that the system will allow before refusing new connections
bufferSize = 1024 # buffer size
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((serverMACAddress, serverPort))
s.listen(serverBacklog)

client, clientAddress = s.accept()
while True:
    recvStr = client.recv(bufferSize).decode().upper()
    if recvStr:
        recvStrList = recvStr.split()
        command = recvStrList[0]
        if command in commandDict.keys():
            try:
                args = recvStrList[1:]
            except IndexError:
                args = []
            returnStr = commandDict[command](args)
            client.send(returnStr.encode())
        else:
            client.send('Invalid Command!'.encode())

print("Closing socket")	
client.close()
s.close()