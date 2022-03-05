import socket
from MotorDriver import *

def motor_config(args):
    try:
        if args[0] == 'SHOW':
            return 'Under Development!'

        elif args[0] == 'ZERO':
            if args[1] == 'LEFT':
                return LMotor.zeroMotor()
            elif args[1] == 'RIGHT':
                return RMotor.zeroMotor()
            elif args[1] == 'BOTH':
                return f'LEFT: {LMotor.zeroMotor()}\nRIGHT: {RMotor.zeroMotor()}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ANGLE':
            if args[1] == 'LEFT':
                return LMotor.setAngleDeg(float(args[2]))
            elif args[1] == 'RIGHT':
                return RMotor.setAngleDeg(float(args[2]))
            elif args[1] == 'BOTH':
                return f'LEFT: {LMotor.setAngleDeg(float(args[2]))}\nRIGHT: {RMotor.setAngleDeg(float(args[2]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'SET':

            if args[2] == 'FREQ':
                if args[1] == 'LEFT':
                    return LMotor.setFlapFreqHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.setFlapFreqHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.setFlapFreqHz(float(args[3]))}\nRIGHT: {RMotor.setFlapFreqHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'AMP':
                if args[1] == 'LEFT':
                    return LMotor.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.setFlapAmplitudeDeg(float(args[3]))}\nRIGHT: {RMotor.setFlapAmplitudeDeg(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'SRATE':
                if args[1] == 'LEFT':
                    return LMotor.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return RMotor.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {LMotor.setFlapSampleRateHz(float(args[3]))}\nRIGHT: {RMotor.setFlapSampleRateHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'
            
            elif args[2] == 'DELAY':
                return 'Under Development!'

            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                return LMotor.runFlapThread(int(args[2]))
            elif args[1] == 'RIGHT':
                return RMotor.runFlapThread(int(args[2]))
            elif args[1] == 'BOTH':
                return 'Under Development!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                return LMotor.stopMotor()
            elif args[1] == 'RIGHT':
                return RMotor.stopMotor()
            elif args[1] == 'BOTH':
                return f'LEFT: {LMotor.stopMotor()}\nRIGHT: {RMotor.stopMotor()}'
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
            'MOTOR START [LEFT|RIGHT|BOTH] [flaps]\n'    
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
LMotor = Motor(pwm_channel=1)

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