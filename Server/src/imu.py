import smbus
import threading
import time

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
        self.sample_period_s = 0.1

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
                time.sleep(self.sample_period_s - (time.time() - time_start))

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
        self.acc_x = self.acc_x_raw/self.ACC_SENSITIVITY_FACTOR 
        self.acc_y = self.acc_y_raw/self.ACC_SENSITIVITY_FACTOR 
        self.acc_z = self.acc_z_raw/self.ACC_SENSITIVITY_FACTOR 
        self.gyro_x = self.gyro_x_raw/self.GYRO_SENSITIVITY_FACTOR
        self.gyro_y = self.gyro_y_raw/self.GYRO_SENSITIVITY_FACTOR
        self.gyro_z = self.gyro_z_raw/self.GYRO_SENSITIVITY_FACTOR

    def get_all_data(self):
        self.acc_x_raw = self.read_raw_data(self.ACCEL_XOUT_H)
        self.acc_y_raw = self.read_raw_data(self.ACCEL_YOUT_H)
        self.acc_z_raw = self.read_raw_data(self.ACCEL_ZOUT_H)
        self.gyro_x_raw = self.read_raw_data(self.GYRO_XOUT_H)
        self.gyro_y_raw = self.read_raw_data(self.GYRO_YOUT_H)
        self.gyro_z_raw = self.read_raw_data(self.GYRO_ZOUT_H)
        self.convert_all_data()