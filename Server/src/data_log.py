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
        self.sample_period_s = 0.1
        self.file_header_str = '\t'.join(['Time', 'Left Motor Set', 'Left Motor Read', 'Right Motor Set', 'Right Motor Read', 'Motor Voltage', 'Motor Current', 'ACC X', 'ACC Y', 'ACC Z', 'GYRO X', 'GYRO Y', 'GYRO Z'])

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            file_name = f'DATA-{time_stamp}.txt'
            time_counter = 0
            with open(f'../data/{file_name}', mode='w', encoding='utf-8') as file:  
                file.write(f'Time: {time_stamp}\n')
                file.write(f'Flap Frequency Set: Left = {round(motor.LeftMotor.MotorUtils.flap_freq_hz, 1)}, Right = {round(motor.RightMotor.MotorUtils.flap_freq_hz, 1)}\n')
                file.write(f'Flap Amplitude Set: Left = {round(motor.LeftMotor.MotorUtils.flap_amplitude_deg, 1)}, Right = {round(motor.RightMotor.MotorUtils.flap_amplitude_deg, 1)}\n')
                file.write(f'Flap Sample Rate Set: Left = {round(motor.LeftMotor.MotorUtils.flap_sample_rate_hz, 1)}, Right = {round(motor.RightMotor.MotorUtils.flap_sample_rate_hz, 1)}\n')
                file.write(f'{self.file_header_str}\n')
                file.flush()
                while True:
                    if self.paused:
                        break
                    time_start = time.time()
                    data_str = '\t'.join([time_counter, 
                        str(round(motor.LeftMotor.MotorUtils.angle_deg, 2)), 
                        str(round(adc.ADCData.adc_left_angle, 2)),
                        str(round(motor.RightMotor.MotorUtils.angle_deg, 2)), 
                        str(round(adc.ADCData.adc_right_angle, 2)),
                        str(round(adc.ADCData.adc_7V4_voltage, 2)),
                        str(round(adc.ADCData.adc_7V4_current, 2)),
                        str(round(imu.IMUData.acc_x, 4)), 
                        str(round(imu.IMUData.acc_y, 4)), 
                        str(round(imu.IMUData.acc_z, 4)), 
                        str(round(imu.IMUData.gyro_x, 4)),
                        str(round(imu.IMUData.gyro_y, 4)),
                        str(round(imu.IMUData.gyro_z, 4))
                    ])
                    file.write(f'{data_str}\n')
                    file.flush()
                    time.sleep((self.sample_period_ms) - (time.time() - time_start))
                    time_counter += self.sample_period_s
                
    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.