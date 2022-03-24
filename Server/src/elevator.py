import RPi.GPIO as GPIO
import threading
import imu

def init():
    global RightElevator, LeftElevator
    RightElevator, LeftElevator = ElevatorThread(gpio_pin=23), ElevatorThread(gpio_pin=24)
    RightElevator.start()
    LeftElevator.start()

class ElevatorThread(threading.Thread):

    # control settings
    GYRO_Y_POS_THRES = 10
    POS_COMPENSATION_ANGLE_DEG = -45
    GYRO_Y_NEG_THRES = -10
    NEG_COMPENSATION_ANGLE_DEG = 45

    def __init__(self, gpio_pin):
        super(ElevatorThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.ElevatorUtils = ElevatorUtils(gpio_pin)

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            while True:
                if self.paused:
                    break
                if imu.IMUData.gyro_y > self.GYRO_Y_POS_THRES:
                    self.ElevatorUtils.set_angle_deg(self.POS_COMPENSATION_ANGLE_DEG)
                elif imu.IMUData.gyro_y < self.GYRO_Y_NEG_THRES:
                    self.ElevatorUtils.set_angle_deg(self.NEG_COMPENSATION_ANGLE_DEG)
                else:
                    self.ElevatorUtils.zero_angle()

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.


class ElevatorUtils:

    # elevator constants
    REFRESH_RATE_HZ = 50

    # limit values
    MAX_ANGLE_DEG = 75
    MIN_ANGLE_DEG = -75
    MAX_ANGLE_PULSE_WIDTH_US = 2000
    MIN_ANGLE_PULSE_WIDTH_US = 1000

    def __init__(self, gpio_pin, reverse_angle=False):

        # setup variables
        self.angle_deg = None
        self.reverse_angle = reverse_angle

        # setup pwm 
        GPIO.setup(gpio_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(gpio_pin, self.REFRESH_RATE_HZ)
        self.pwm.start(0) # initialize pwm at 0% duty

    def pulse_width_to_duty(self, pulse_width_us):
        return 100*pulse_width_us*1e-6*self.REFRESH_RATE_HZ

    def angle_to_pulse_width(self, angle_deg):
        return self.MIN_ANGLE_PULSE_WIDTH_US + (angle_deg - self.MIN_ANGLE_DEG)*((self.MAX_ANGLE_PULSE_WIDTH_US - self.MIN_ANGLE_PULSE_WIDTH_US)/(self.MAX_ANGLE_DEG - self.MIN_ANGLE_DEG))

    def angle_to_duty(self, angle_deg):
        return self.pulse_width_to_duty(self.angle_to_pulse_width(angle_deg))    

    def set_angle_deg(self, angle_deg):
        if self.reverse_angle:
            angle_deg = -1*angle_deg
        if (angle_deg < self.MIN_ANGLE_DEG) or (angle_deg > self.MAX_ANGLE_DEG):
            return 'Invalid angle!'
        else:
            try:
                self.pwm.ChangeDutyCycle(self.angle_to_duty(angle_deg))
                self.angle_deg = angle_deg
                return 'Success!'
            except:
                return 'Error Occurred!'

    def zero_angle(self):
        return self.set_angle_deg(0)

    def stop(self):
        try:
            self.pwm.ChangeDutyCycle(0)
            self.angle_deg = None
            return 'Success!'
        except: 
            return 'Error Occurred!'