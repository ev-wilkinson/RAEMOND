import time
import motor
import adc
import imu
import elevator
import data_log

def init():
    global command_dict # setup commands dictionary
    command_dict = {'HELP': print_help,
                   'MOTOR': motor_config,
                   'ADC': adc_config,
                   'IMU': imu_config,
                   'ELEVATOR': elevator_config,
                   'LOG': log_config
    }

def motor_config(args):
    try:
        if args[0] == 'SHOW':
            if args[1] == 'LEFT':
                if motor.LeftMotor.MotorUtils.angle_deg is None:
                    print_angle = 'None'
                else:
                    print_angle = str(round(motor.LeftMotor.MotorUtils.angle_deg, 1)) + ' degrees'
                return (f'Angle Set: {print_angle}\n'
                        f'Angle Read: {round(adc.ADCData.adc_left_angle, 1)} degrees\n'
                        f'Flap Frequency: {round(motor.LeftMotor.MotorUtils.flap_freq_hz, 1)} Hz\n'
                        f'Flap Amplitude: {round(motor.LeftMotor.MotorUtils.flap_amplitude_deg, 1)} degrees\n'
                        f'Sample Rate: {round(motor.LeftMotor.MotorUtils.flap_sample_rate_hz, 1)} Hz\n'
                        f'Running: {not motor.LeftMotor.paused}\n'
                        '\nSuccess!')
            elif args[1] == 'RIGHT':
                if motor.RightMotor.MotorUtils.angle_deg is None:
                    print_angle = 'None'
                else:
                    print_angle = str(round(motor.RightMotor.MotorUtils.angle_deg, 1)) + ' degrees'
                return (f'Angle Set: {print_angle}\n'
                        f'Angle Read: {round(adc.ADCData.adc_right_angle, 1)} degrees\n'
                        f'Flap Frequency: {round(motor.RightMotor.MotorUtils.flap_freq_hz, 1)} Hz\n'
                        f'Flap Amplitude: {round(motor.RightMotor.MotorUtils.flap_amplitude_deg, 1)} degrees\n'
                        f'Sample Rate: {round(motor.RightMotor.MotorUtils.flap_sample_rate_hz, 1)} Hz\n'
                        f'Running: {not motor.RightMotor.paused}\n'
                        '\nSuccess!')
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ZERO':
            if args[1] == 'LEFT':
                motor.LeftMotor.pause()
                return motor.LeftMotor.MotorUtils.zero_angle()
            elif args[1] == 'RIGHT':
                motor.RightMotor.pause()
                return motor.RightMotor.MotorUtils.zero_angle()
            elif args[1] == 'BOTH':
                motor.LeftMotor.pause()
                motor.RightMotor.pause()
                return f'LEFT: {motor.LeftMotor.MotorUtils.zero_angle()}\nRIGHT: {motor.RightMotor.MotorUtils.zero_angle()}'
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

        elif args[0] == 'FREQ':
            if args[1] == 'LEFT':
                return motor.LeftMotor.MotorUtils.set_flap_freq_hz(float(args[3]))
            elif args[1] == 'RIGHT':
                return motor.RightMotor.MotorUtils.set_flap_freq_hz(float(args[3]))
            elif args[1] == 'BOTH':
                return f'LEFT: {motor.LeftMotor.MotorUtils.set_flap_freq_hz(float(args[3]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_flap_freq_hz(float(args[3]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'AMPLITUDE':
            if args[1] == 'LEFT':
                return motor.LeftMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))
            elif args[1] == 'RIGHT':
                return motor.RightMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))
            elif args[1] == 'BOTH':
                return f'LEFT: {motor.LeftMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))}\nRIGHT: {motor.RightMotor.MotorUtils.set_flap_amplitude_deg(float(args[3]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                motor.LeftMotor.MotorUtils.zero_angle()
                time.sleep(1)
                motor.LeftMotor.resume()
                return 'Success!'
            elif args[1] == 'RIGHT':
                motor.RightMotor.MotorUtils.zero_angle()
                time.sleep(1)
                motor.RightMotor.resume()
                return 'Success!'
            elif args[1] == 'BOTH':
                motor.LeftMotor.MotorUtils.zero_angle()
                motor.RightMotor.MotorUtils.zero_angle()
                time.sleep(1)
                motor.LeftMotor.resume()
                motor.RightMotor.resume()
                return 'Success!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                motor.LeftMotor.pause()
                return motor.LeftMotor.MotorUtils.stop()
            elif args[1] == 'RIGHT':
                motor.RightMotor.pause()
                return motor.RightMotor.MotorUtils.stop()
            elif args[1] == 'BOTH':
                motor.LeftMotor.pause()
                motor.RightMotor.pause()
                return f'LEFT: {motor.LeftMotor.MotorUtils.stop()}\nRIGHT: {motor.RightMotor.MotorUtils.stop()}'
            else:
                return 'Invalid Command Arguments!'
        
        else:
            return 'Invalid Command Arguments!'

    except IndexError:
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

def adc_config(args):
    try:
        if args[0] == 'DATA':
            paused = adc.ADCCtrl.paused # get initial pause state
            adc.ADCCtrl.pause()
            adc.ADCData.get_all_data()
            if not paused: 
                adc.ADCCtrl.resume() # restore if previously running
            return (f'7V4 Current: {round(adc.ADCData.adc_7V4_current, 4)} A\n'
                    f'7V4 Voltage: {round(adc.ADCData.adc_7V4_voltage, 2)} V\n'
                    f'5V Voltage: {round(adc.ADCData.adc_5V_voltage, 2)} V\n'
                    f'Left Angle: {round(adc.ADCData.adc_left_angle, 1)} degrees\n'
                    f'Right Angle: {round(adc.ADCData.adc_right_angle, 1)} degrees\n'
                    '\nSuccess!')

        elif args[0] == 'RAW':
            paused = adc.ADCCtrl.paused # get initial pause state
            adc.ADCCtrl.pause()
            adc.ADCData.get_all_data()
            if not paused: 
                adc.ADCCtrl.resume() # restore if previously running
            return (f'CH0: {round(adc.ADCData.adc_ch0_raw, 4)} V\n'
                    f'CH1: {round(adc.ADCData.adc_ch1_raw, 4)} V\n'
                    f'CH2: {round(adc.ADCData.adc_ch2_raw, 4)} V\n'
                    f'CH3: {round(adc.ADCData.adc_ch3_raw, 4)} V\n'
                    f'CH4: {round(adc.ADCData.adc_ch4_raw, 4)} V\n'
                    '\nSuccess!')
        else:
            return 'Invalid Command Arguments!'
        
    except IndexError:  
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

def imu_config(args):
    try:
        if args[0] == 'DATA':
            paused = imu.IMUCtrl.paused # get initial pause state
            imu.IMUCtrl.pause()
            imu.IMUData.get_all_data()
            if not paused: 
                imu.IMUCtrl.resume() # restore if previously running
            return (f'ACC X: {round(imu.IMUData.acc_x, 4)} g\n'
                    f'ACC Y: {round(imu.IMUData.acc_y, 4)} g\n'
                    f'ACC Z: {round(imu.IMUData.acc_z, 4)} g\n'
                    f'GYRO X: {round(imu.IMUData.gyro_x, 4)} deg/s\n'
                    f'GYRO Y: {round(imu.IMUData.gyro_y, 4)} deg/s\n'
                    f'GYRO Z: {round(imu.IMUData.gyro_z, 4)} deg/s\n'
                    f'Roll: {round(imu.IMUData.roll_angle_deg, 2)} degrees\n'
                    f'Pitch: {round(imu.IMUData.pitch_angle_deg, 2)} degrees\n'
                    '\nSuccess!')

        elif args[0] == 'RAW':
            paused = imu.IMUCtrl.paused # get initial pause state
            imu.IMUCtrl.pause()
            imu.IMUData.get_all_data()
            if not paused: 
                imu.IMUCtrl.resume() # restore if previously running
            return (f'ACC X raw: {round(imu.IMUData.acc_x_raw, 4)} g\n'
                    f'ACC raw: {round(imu.IMUData.acc_y_raw, 4)} g\n'
                    f'ACC Z raw: {round(imu.IMUData.acc_z_raw, 4)} g\n'
                    f'GYRO X raw: {round(imu.IMUData.gyro_x_raw, 4)} deg/s\n'
                    f'GYRO Y raw: {round(imu.IMUData.gyro_y_raw, 4)} deg/s\n'
                    f'GYRO Z raw: {round(imu.IMUData.gyro_z_raw, 4)} deg/s\n'
                    '\nSuccess!')
        else:
            return 'Invalid Command Arguments!'
        
    except IndexError:  
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

def elevator_config(args):
    try:
        if args[0] == 'SHOW':
            if args[1] == 'LEFT':
                if elevator.LeftElevator.ElevatorUtils.angle_deg is None:
                    print_angle = 'None'
                else:
                    print_angle = str(round(elevator.LeftElevator.ElevatorUtils.angle_deg, 1)) + ' degrees'
                return (f'Angle Set: {print_angle}\n'
                        f'Running: {not elevator.LeftElevator.paused}\n'
                        '\nSuccess!')
            elif args[1] == 'RIGHT':
                if elevator.RightElevator.ElevatorUtils.angle_deg is None:
                    print_angle = 'None'
                else:
                    print_angle = str(round(elevator.RightElevator.ElevatorUtils.angle_deg, 1)) + ' degrees'
                return (f'Angle Set: {print_angle}\n'
                        f'Running: {not elevator.RightElevator.paused}\n'
                        '\nSuccess!')
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ZERO':
            if args[1] == 'LEFT':
                elevator.LeftElevator.pause()
                return elevator.LeftElevator.ElevatorUtils.zero_angle()
            elif args[1] == 'RIGHT':
                elevator.RightElevator.pause()
                return elevator.RightElevator.ElevatorUtils.zero_angle()
            elif args[1] == 'BOTH':
                elevator.LeftElevator.pause()
                elevator.RightElevator.pause()
                return f'LEFT: {elevator.LeftElevator.ElevatorUtils.zero_angle()}\nRIGHT: {elevator.RightElevator.ElevatorUtils.zero_angle()}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'ANGLE':
            if args[1] == 'LEFT':
                elevator.LeftElevator.pause()
                return elevator.LeftElevator.ElevatorUtils.set_angle_deg(float(args[2]))
            elif args[1] == 'RIGHT':
                elevator.RightElevator.pause()
                return elevator.RightElevator.ElevatorUtils.set_angle_deg(float(args[2]))
            elif args[1] == 'BOTH':
                elevator.LeftElevator.pause()
                elevator.RightElevator.pause()
                return f'LEFT: {elevator.LeftElevator.ElevatorUtils.set_angle_deg(float(args[2]))}\nRIGHT: {elevator.RightElevator.ElevatorUtils.set_angle_deg(float(args[2]))}'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'START':   
            if args[1] == 'LEFT':
                elevator.LeftElevator.ElevatorUtils.zero_angle()
                time.sleep(1)
                elevator.LeftElevator.resume()
                return 'Success!'
            elif args[1] == 'RIGHT':
                elevator.RightElevator.ElevatorUtils.zero_angle()
                time.sleep(1)
                elevator.RightElevator.resume()
                return 'Success!'
            elif args[1] == 'BOTH':
                elevator.LeftElevator.ElevatorUtils.zero_angle()
                elevator.RightElevator.ElevatorUtils.zero_angle()
                time.sleep(1)
                elevator.LeftElevator.resume()
                elevator.RightElevator.resume()
                return 'Success!'
            else:
                return 'Invalid Command Arguments!'

        elif args[0] == 'STOP':   
            if args[1] == 'LEFT':
                elevator.LeftElevator.pause()
                return elevator.LeftElevator.ElevatorUtils.stop()
            elif args[1] == 'RIGHT':
                elevator.RightElevator.pause()
                return elevator.RightElevator.ElevatorUtils.stop()
            elif args[1] == 'BOTH':
                elevator.LeftElevator.pause()
                elevator.RightElevator.pause()
                return f'LEFT: {elevator.LeftElevator.ElevatorUtils.stop()}\nRIGHT: {elevator.RightElevator.ElevatorUtils.stop()}'
            else:
                return 'Invalid Command Arguments!'
        
        else:
            return 'Invalid Command Arguments!'

    except IndexError:
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

def log_config(args):
    try:
        if args[0] == 'START': 
            data_log.FileWriter.resume()
            return 'Success!'
        elif args[0] == 'STOP':
            data_log.FileWriter.pause()
            return 'Success!'
        else:
            return 'Invalid Command Arguments!' 
    except IndexError:
        return 'Invalid Command Arguments!'
    except:         
        return 'Error Ocurred!'

def print_help(args):
    return ('\nCommands:\n'
            'HELP\n'                                                                    
            'MOTOR SHOW [LEFT|RIGHT]\n'             
            'MOTOR ZERO [LEFT|RIGHT|BOTH]\n'             
            'MOTOR ANGLE [LEFT|RIGHT|BOTH] [value in degrees]\n'
            'MOTOR FREQ [LEFT|RIGHT|BOTH] [value in hz]\n'
            'MOTOR AMPLITUDE [LEFT|RIGHT|BOTH] [value in degrees]\n'
            'MOTOR START [LEFT|RIGHT|BOTH]\n'    
            'MOTOR STOP [LEFT|RIGHT|BOTH]\n'             
            'ADC [DATA|RAW]\n'                                 
            'IMU [DATA|RAW]\n'                                 
            'ELEVATOR SHOW [LEFT|RIGHT]\n'             
            'ELEVATOR ZERO [LEFT|RIGHT|BOTH]\n'        
            'ELEVATOR ANGLE [LEFT|RIGHT|BOTH] [value in degrees]\n'
            'ELEVATOR START [LEFT|RIGHT|BOTH]\n'
            'ELEVATOR STOP [LEFT|RIGHT|BOTH]\n'                      
            'LOG START\n'
            'LOG STOP\n'                           
    )