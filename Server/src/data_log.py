# data_log.py
# Description: thread for writing data to csv file
# Author: Evan Wilkinson

# standard libraries
import csv
import threading
import time
import datetime

# modules
import motor
import adc
import imu
import elevator
import settings

def init():
    global FileWriter
    FileWriter = FileWriteThread()
    FileWriter.start() # start thread

class FileWriteThread(threading.Thread):
    def __init__(self):
        super(FileWriteThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.file_header_list = ['Time', 'Left Motor Set', 'Left Motor Read', 'Right Motor Set', 'Right Motor Read', 'Left Elevator Set', 'Right Elevator Set',
                                 'Voltage', 'Current', 'ACC X', 'ACC Y', 'ACC Z', 'GYRO X', 'GYRO Y', 'GYRO Z', 'Roll', 'Pitch']

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            file_name = f'DATA-{time_stamp}.csv'
            time_counter = 0
            # create csv file in Server/data/ folder
            with open(f'../data/{file_name}', mode='w', newline='') as file:  
                writer = csv.writer(file)
                writer.writerow(['Time', time_stamp])
                writer.writerow(['Left Flap Frequency Set', f'{round(motor.LeftMotor.MotorUtils.flap_freq_hz, 1)} Hz'])
                writer.writerow(['Right Flap Frequency Set', f'{round(motor.RightMotor.MotorUtils.flap_freq_hz, 1)} Hz'])
                writer.writerow(['Left Flap Amplitude Set', f'{round(motor.LeftMotor.MotorUtils.flap_amplitude_deg, 1)} degrees'])
                writer.writerow(['Right Flap Amplitude Set', f'{round(motor.RightMotor.MotorUtils.flap_amplitude_deg, 1)} degrees'])
                writer.writerow(self.file_header_list)
                file.flush()
                while True:
                    if self.paused:
                        break
                    time_start = time.time()
                    # check if data is not type float
                    if motor.LeftMotor.MotorUtils.angle_deg is None:
                        left_motor_angle = 'None'
                    else:
                        left_motor_angle = round(motor.LeftMotor.MotorUtils.angle_deg, 2)
                    if motor.RightMotor.MotorUtils.angle_deg is None:
                        right_motor_angle = 'None'
                    else:
                        right_motor_angle = round(motor.RightMotor.MotorUtils.angle_deg, 2)
                    if elevator.LeftElevator.ElevatorUtils.angle_deg is None:
                        left_elevator_angle = 'None'
                    else:
                        left_elevator_angle = round(elevator.LeftElevator.ElevatorUtils.angle_deg, 2)
                    if elevator.RightElevator.ElevatorUtils.angle_deg is None:
                        right_elevator_angle = 'None'
                    else:
                        right_elevator_angle = round(elevator.RightElevator.ElevatorUtils.angle_deg, 2)
                    # create list of data
                    data_list = [round(time_counter, 2), left_motor_angle, round(adc.ADCData.adc_left_angle, 2), right_motor_angle, round(adc.ADCData.adc_right_angle, 2),
                                 left_elevator_angle, right_elevator_angle,
                                 round(adc.ADCData.adc_7V4_voltage, 4), round(adc.ADCData.adc_7V4_current, 4),
                                 round(imu.IMUData.acc_x, 4), round(imu.IMUData.acc_y, 4), round(imu.IMUData.acc_z, 4), round(imu.IMUData.gyro_x, 4), round(imu.IMUData.gyro_y, 4), round(imu.IMUData.gyro_z, 4),
                                 round(imu.IMUData.roll_angle_deg, 2), round(imu.IMUData.pitch_angle_deg, 2)]
                    writer.writerow(data_list) # write data to file
                    file.flush() # save file
                    try: 
                        time.sleep((1/settings.LOG_SAMPLE_RATE_HZ) - (time.time() - time_start)) # delay for sample rate timing
                    except ValueError:
                        pass
                    time_counter += 1/settings.LOG_SAMPLE_RATE_HZ
                
    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.