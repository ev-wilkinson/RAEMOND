import RPi.GPIO as GPIO
import threading
import imu
import time
import settings

def init():
    global RightElevator, LeftElevator
    RightElevator, LeftElevator = ElevatorThread(gpio_pin=23, zero_offset=settings.RIGHT_ELEV_ZERO_OFFSET), ElevatorThread(gpio_pin=24, zero_offset=settings.LEFT_ELEV_ZERO_OFFSET, reverse_angle=True)
    RightElevator.start()
    LeftElevator.start()

class ElevatorThread(threading.Thread):

    def __init__(self, gpio_pin, zero_offset, reverse_angle=False):
        super(ElevatorThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.ElevatorUtils = ElevatorUtils(gpio_pin, zero_offset, reverse_angle)

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            while True:
                if self.paused:
                    break
                correction_angle_deg = -1*imu.IMUData.pitch_angle_deg*settings.ELEV_CORR_ANGLE_FACTOR
                if settings.ELEV_CORR_ANGLE_DEG_MIN <= correction_angle_deg <= settings.ELEV_CORR_ANGLE_DEG_MAX:
                    self.ElevatorUtils.set_angle_deg(correction_angle_deg)
                elif correction_angle_deg < settings.ELEV_CORR_ANGLE_DEG_MIN:
                    self.ElevatorUtils.set_angle_deg(settings.ELEV_CORR_ANGLE_DEG_MIN)
                elif correction_angle_deg > settings.ELEV_CORR_ANGLE_DEG_MAX:
                    self.ElevatorUtils.set_angle_deg(settings.ELEV_CORR_ANGLE_DEG_MAX)
                time.sleep(settings.ELEV_CORR_PERIOD_S)

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

    def __init__(self, gpio_pin, zero_offset, reverse_angle=False):

        # setup variables
        self.angle_deg = None
        self.reverse_angle = reverse_angle
        self.zero_offset = zero_offset 

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
                self.pwm.ChangeDutyCycle(self.angle_to_duty(angle_deg+self.zero_offset))
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