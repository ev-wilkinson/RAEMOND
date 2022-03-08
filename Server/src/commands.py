import MotorDriver

def init():

    # setup commands dictionary
    global commandDict
    commandDict = {'HELP': print_help,
                   'MOTOR': motor_config,
                   'ADC': adc_config,
                   'IMU': imu_config,
                   'ELEVATOR': elevator_config,
                   'TERMINATE': terminate_program
    }

def motor_config(args):
    try:
        if args[0] == 'SHOW':
            return 'Under Development!'

        elif args[0] == 'ZERO':
            if args[1] == 'LEFT':
                MotorDriver.LMotor.pause()
                return MotorDriver.LMotor.motorUtils.zeroMotor()
            elif args[1] == 'RIGHT':
                MotorDriver.RMotor.pause()
                return MotorDriver.RMotor.motorUtils.zeroMotor()
            elif args[1] == 'BOTH':
                MotorDriver.LMotor.pause()
                MotorDriver.RMotor.pause()
                return f'LEFT: {MotorDriver.LMotor.motorUtils.zeroMotor()}\nRIGHT: {MotorDriver.RMotor.motorUtils.zeroMotor()}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ANGLE':
            if args[1] == 'LEFT':
                MotorDriver.LMotor.pause()
                return MotorDriver.LMotor.motorUtils.setAngleDeg(float(args[2]))
            elif args[1] == 'RIGHT':
                MotorDriver.RMotor.pause()
                return MotorDriver.RMotor.motorUtils.setAngleDeg(float(args[2]))
            elif args[1] == 'BOTH':
                MotorDriver.LMotor.pause()
                MotorDriver.RMotor.pause()
                return f'LEFT: {MotorDriver.LMotor.motorUtils.setAngleDeg(float(args[2]))}\nRIGHT: {MotorDriver.RMotor.motorUtils.setAngleDeg(float(args[2]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'SET':

            if args[2] == 'FREQ':
                if args[1] == 'LEFT':
                    return MotorDriver.LMotor.motorUtils.setFlapFreqHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return MotorDriver.RMotor.motorUtils.setFlapFreqHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {MotorDriver.LMotor.motorUtils.setFlapFreqHz(float(args[3]))}\nRIGHT: {MotorDriver.RMotor.motorUtils.setFlapFreqHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'AMP':
                if args[1] == 'LEFT':
                    return MotorDriver.LMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'RIGHT':
                    return MotorDriver.RMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {MotorDriver.LMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))}\nRIGHT: {MotorDriver.RMotor.motorUtils.setFlapAmplitudeDeg(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'SRATE':
                if args[1] == 'LEFT':
                    return MotorDriver.LMotor.motorUtils.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return MotorDriver.RMotor.motorUtils.setFlapSampleRateHz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {MotorDriver.LMotor.motorUtils.setFlapSampleRateHz(float(args[3]))}\nRIGHT: {MotorDriver.RMotor.motorUtils.setFlapSampleRateHz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'
            
            elif args[2] == 'DELAY':
                return 'Under Development!'

            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                try:
                    MotorDriver.LMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'RIGHT':
                try:
                    MotorDriver.RMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'BOTH':
                try:
                    MotorDriver.LMotor.resume()
                    MotorDriver.RMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                MotorDriver.LMotor.pause()
                return MotorDriver.LMotor.motorUtils.stopMotor()
            elif args[1] == 'RIGHT':
                MotorDriver.RMotor.pause()
                return MotorDriver.RMotor.motorUtils.stopMotor()
            elif args[1] == 'BOTH':
                MotorDriver.LMotor.pause()
                MotorDriver.RMotor.pause()
                return f'LEFT: {MotorDriver.LMotor.motorUtils.stopMotor()}\nRIGHT: {MotorDriver.RMotor.motorUtils.stopMotor()}'
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