import csv
import threading
import time
import datetime
import motor
import adc
import imu

def init():
    global FileWriter
    FileWriter = FileWriteThread()
    FileWriter.start()

class FileWriteThread(threading.Thread):
    def __init__(self):
        super(FileWriteThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.sample_rate_hz = 20
        self.file_header_list = ['Time', 'Left Set', 'Left Read', 'Right Set', 'Right Read', 'Voltage', 'Current', 'ACC X', 'ACC Y', 'ACC Z', 'GYRO X', 'GYRO Y', 'GYRO Z']

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            file_name = f'DATA-{time_stamp}.csv'
            time_counter = 0
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
                    if motor.LeftMotor.MotorUtils.angle_deg is None:
                        left_angle = 'None'
                    else:
                        left_angle = round(motor.LeftMotor.MotorUtils.angle_deg, 2)
                    if motor.RightMotor.MotorUtils.angle_deg is None:
                        right_angle = 'None'
                    else:
                        right_angle = round(motor.RightMotor.MotorUtils.angle_deg, 2)
                    data_list = [round(time_counter, 2), left_angle, round(adc.ADCData.adc_left_angle, 2), right_angle, round(adc.ADCData.adc_right_angle, 2),
                                 round(adc.ADCData.adc_7V4_voltage, 4), round(adc.ADCData.adc_7V4_current, 4),
                                 round(imu.IMUData.acc_x, 4), round(imu.IMUData.acc_y, 4), round(imu.IMUData.acc_z, 4), round(imu.IMUData.gyro_x, 4), round(imu.IMUData.gyro_y, 4), round(imu.IMUData.gyro_z, 4)]
                    writer.writerow(data_list)
                    file.flush()
                    time.sleep((1/self.sample_rate_hz) - (time.time() - time_start))
                    time_counter += 1/self.sample_rate_hz
                
    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.