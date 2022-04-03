import smbus
import threading
import time
import math

def init():
    global IMUData, IMUCtrl
    IMUData = IMU()
    IMUCtrl = IMUThread()
    IMUCtrl.start()

class IMUThread(threading.Thread):
    def __init__(self):
        super(IMUThread, self).__init__()
        self.paused = False  # Start out running.
        self.state = threading.Condition()
        self.sample_rate_hz = 20

    def run(self):
        global IMUData
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            while True:
                if self.paused:
                    break
                time_start = time.time()
                IMUData.get_all_data()
                try:
                    time.sleep((1/self.sample_rate_hz) - (time.time() - time_start))
                except ValueError:
                    pass 

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.


class IMU:

    # i2c constants
    I2C_PORT = 1 
    DEVICE_ADR = 0x68

    # MPU6050 Registers and their Address
    PWR_MGMT_1     = 0x6B
    SMPLRT_DIV     = 0x19
    CONFIG         = 0x1A
    GYRO_CONFIG    = 0x1B
    INT_ENABLE     = 0x38
    ACCEL_XOUT_H   = 0x3B
    ACCEL_YOUT_H   = 0x3D
    ACCEL_ZOUT_H   = 0x3F
    GYRO_XOUT_H    = 0x43
    GYRO_YOUT_H    = 0x45
    GYRO_ZOUT_H    = 0x47

    # sensor constants
    ACC_SENSITIVITY_FACTOR = 16384.0
    GYRO_SENSITIVITY_FACTOR = 131.0
    PITCH_OFFSET = -5.2
    ROLL_OFFSET = -1.0 

    def __init__(self):

        # setup imu variables
        self.acc_x_raw = None
        self.acc_y_raw = None
        self.acc_z_raw = None
        self.gyro_x_raw = None
        self.gyro_y_raw = None
        self.gyro_z_raw = None
        self.acc_x = None
        self.acc_y = None
        self.acc_z = None
        self.gyro_x = None
        self.gyro_y = None
        self.gyro_z = None
        self.pitch_angle_deg = None
        self.roll_angle_deg = None

        # initialize i2c
        self.i2c = smbus.SMBus(self.I2C_PORT)

        # configure MPU6050 Registers
        self.mpu_init()

        # get intital values
        self.get_all_data()


    def mpu_init(self):
        self.i2c.write_byte_data(self.DEVICE_ADR, self.SMPLRT_DIV, 7) # write to sample rate register
        self.i2c.write_byte_data(self.DEVICE_ADR, self.PWR_MGMT_1, 1) # write to power management register
        self.i2c.write_byte_data(self.DEVICE_ADR, self.CONFIG, 0) # write to Configuration register
        self.i2c.write_byte_data(self.DEVICE_ADR, self.GYRO_CONFIG, 24) # write to Gyro configuration register
        self.i2c.write_byte_data(self.DEVICE_ADR, self.INT_ENABLE, 1) # write to interrupt enable register

    def read_raw_data(self, addr):
        high = self.i2c.read_byte_data(self.DEVICE_ADR, addr)
        low = self.i2c.read_byte_data(self.DEVICE_ADR, addr+1)
        value = ((high << 8) | low) #concatenate higher and lower value
        if(value > 32768):
            value = value - 65536 # to get signed value from mpu6050
        return value

    def convert_all_data(self):
        self.acc_x = -1*self.acc_x_raw/self.ACC_SENSITIVITY_FACTOR 
        self.acc_y = -1*self.acc_y_raw/self.ACC_SENSITIVITY_FACTOR 
        self.acc_z = -1*self.acc_z_raw/self.ACC_SENSITIVITY_FACTOR 
        self.gyro_x = -1*self.gyro_x_raw/self.GYRO_SENSITIVITY_FACTOR
        self.gyro_y = -1*self.gyro_y_raw/self.GYRO_SENSITIVITY_FACTOR
        self.gyro_z = -1*self.gyro_z_raw/self.GYRO_SENSITIVITY_FACTOR

    def get_all_data(self):
        self.acc_x_raw = self.read_raw_data(self.ACCEL_XOUT_H)
        self.acc_y_raw = self.read_raw_data(self.ACCEL_YOUT_H)
        self.acc_z_raw = self.read_raw_data(self.ACCEL_ZOUT_H)
        self.gyro_x_raw = self.read_raw_data(self.GYRO_XOUT_H)
        self.gyro_y_raw = self.read_raw_data(self.GYRO_YOUT_H)
        self.gyro_z_raw = self.read_raw_data(self.GYRO_ZOUT_H)
        self.convert_all_data()
        self.get_pitch_angle()
        self.get_roll_angle()

    def get_dist(self, a, b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.get_dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.get_dist(x,z))
        return math.degrees(radians)

    def get_pitch_angle(self):
        self.pitch_angle_deg = self.get_y_rotation(self.acc_x, self.acc_y, self.acc_z) + self.PITCH_OFFSET

    def get_roll_angle(self):
        self.roll_angle_deg = self.get_x_rotation(self.acc_x, self.acc_y, self.acc_z) + self.ROLL_OFFSET