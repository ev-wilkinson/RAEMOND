import motor
import adc

def init():

    # setup commands dictionary
    global command_dict
    command_dict = {'HELP': print_help,
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
                motor.LeftMotor.pause()
                return motor.LeftMotor.MotorUtils.zero_motor()
            elif args[1] == 'RIGHT':
                motor.RightMotor.pause()
                return motor.RightMotor.MotorUtils.zero_motor()
            elif args[1] == 'BOTH':
                motor.LeftMotor.pause()
                motor.RightMotor.pause()
                return f'LEFT: {motor.LeftMotor.MotorUtils.zero_motor()}\nRIGHT: {motor.RightMotor.MotorUtils.zero_motor()}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ANGLE':
            if args[1] == 'LEFT':
                motor.LeftMotor.pause()
                return motor.LeftMotor.MotorUtils.set_angle_deg(float(args[2]))
            elif args[1] == 'RIGHT':
                motor.RightMotor.pause()
                return motor.RightMotor.MotorUtils.set_angle_deg(float(args[2]))
            elif args[1] == 'BOTH':
                motor.LeftMotor.pause()
                motor.RightMotor.pause()
                return f'LEFT: {motor.LeftMotor.MotorUtils.set_angle_deg(float(args[2]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_angle_deg(float(args[2]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'SET':

            if args[2] == 'FREQ':
                if args[1] == 'LEFT':
                    return motor.LeftMotor.MotorUtils.set_flap_freq_hz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return motor.RightMotor.MotorUtils.set_flap_freq_hz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {motor.LeftMotor.MotorUtils.set_flap_freq_hz(float(args[3]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_flap_freq_hz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'AMP':
                if args[1] == 'LEFT':
                    return motor.LeftMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))
                elif args[1] == 'RIGHT':
                    return motor.RightMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {motor.LeftMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'

            elif args[2] == 'SRATE':
                if args[1] == 'LEFT':
                    return motor.LeftMotor.MotorUtils.set_flap_sample_rate_hz(float(args[3]))
                elif args[1] == 'RIGHT':
                    return motor.RightMotor.MotorUtils.set_flap_sample_rate_hz(float(args[3]))
                elif args[1] == 'BOTH':
                    return f'LEFT: {motor.LeftMotor.MotorUtils.set_flap_sample_rate_hz(float(args[3]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_flap_sample_rate_hz(float(args[3]))}'
                else:
                    return 'Invalid Command Arguments!'
            
            elif args[2] == 'DELAY':
                return 'Under Development!'

            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                try:
                    motor.LeftMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'RIGHT':
                try:
                    motor.RightMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            elif args[1] == 'BOTH':
                try:
                    motor.LeftMotor.resume()
                    motor.RightMotor.resume()
                    return 'Success!'
                except:
                    return 'Error Occurred!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                motor.LeftMotor.pause()
                return motor.LeftMotor.MotorUtils.stop_motor()
            elif args[1] == 'RIGHT':
                motor.RightMotor.pause()
                return motor.RightMotor.MotorUtils.stop_motor()
            elif args[1] == 'BOTH':
                motor.LeftMotor.pause()
                motor.RightMotor.pause()
                return f'LEFT: {motor.LeftMotor.MotorUtils.stop_motor()}\nRIGHT: {motor.RightMotor.MotorUtils.stop_motor()}'
            else:
                return 'Invalid Command Arguments!'
        
        else:
            return 'Invalid Command Arguments!'

    except IndexError:
        return 'Invalid Command Arguments!'

def adc_config(args):
    try:
        if args[0] == 'DATA':
            return (f'7V4 Current: {round(adc.ADCData.get_7V4_current(), 4)} A\n'
                    f'7V4 Voltage: {round(adc.ADCData.get_7V4_voltage(), 2)} V\n'
                    f'5V Voltage: {round(adc.ADCData.get_5V_voltage(), 2)} V\n'
                    f'Left Angle: {round(adc.ADCData.get_left_angle(), 1)} degrees\n'
                    f'Right Angle: {round(adc.ADCData.get_right_angle(), 1)} degrees\n'
                    '\nSuccess!')
        elif args[0] == 'RAW':
            return (f'CH0: {round(adc.ADCData.get_adc_voltage(adc.ADCData.ADC_CH0), 4)} V\n'
                    f'CH1: {round(adc.ADCData.get_adc_voltage(adc.ADCData.ADC_CH1), 4)} V\n'
                    f'CH2: {round(adc.ADCData.get_adc_voltage(adc.ADCData.ADC_CH2), 4)} V\n'
                    f'CH3: {round(adc.ADCData.get_adc_voltage(adc.ADCData.ADC_CH3), 4)} V\n'
                    f'CH4: {round(adc.ADCData.get_adc_voltage(adc.ADCData.ADC_CH4), 4)} V\n'
                    '\nSuccess!')
        else:
            return 'Invalid Command Arguments!'
        
    except IndexError:  
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

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
            'ADC [DATA|RAW]\n'                                 
            'IMU SHOW\n'                                 
            'ELEVATOR SET [value]\n'                     
            'ELEVATOR SHOW\n'                            
    )