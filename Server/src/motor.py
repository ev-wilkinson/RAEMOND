from rpi_hardware_pwm import HardwarePWM
import threading
import numpy as np
import time

def init():

    # initiliaze motors
    global RightMotor, LeftMotor
    RightMotor, LeftMotor = MotorThread(pwm_channel=0), MotorThread(pwm_channel=1)
    RightMotor.start()
    LeftMotor.start()

class MotorThread(threading.Thread):
    def __init__(self, pwm_channel):
        super(MotorThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.MotorUtils = MotorUtils(pwm_channel)

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            for angle in self.MotorUtils.flap_angle_array:
                if self.paused:
                    break
                time_start = time.time()
                self.MotorUtils.set_angle_deg(angle)
                try:
                    time.sleep((1/self.MotorUtils.flap_sample_rate_hz) - (time.time() - time_start))
                except ValueError:
                    pass    

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

class MotorUtils:

    # motor constants
    REFRESH_RATE_HZ = 333

    # limit values
    MAX_ANGLE_DEG = 65
    MIN_ANGLE_DEG = -65
    MAX_ANGLE_PULSE_WIDTH_US = 2100
    MIN_ANGLE_PULSE_WIDTH_US = 900
    MAX_FLAP_FREQ_HZ = 2
    MIN_FLAP_FREQ_HZ = 0
    MAX_FLAP_SAMPLE_RATE_HZ = 200
    MIN_FLAP_SAMPLE_RATE_HZ = 0

    def __init__(self, pwm_channel):

        self.angle_deg = None
        self.flap_freq_hz = 0.5
        #self.flap_delay_sec = 0
        self.flap_amplitude_deg = 60
        self.flap_sample_rate_hz = 20
        self.flap_angle_array = None
        self.update_flap_angle_array()

        self.pwm = HardwarePWM(pwm_channel=pwm_channel, hz=self.REFRESH_RATE_HZ)
        self.pwm.start(0) # initialize pwm at 0% duty

    def pulse_width_to_duty(self, pulse_width_us):
        return 100*pulse_width_us*1e-6*self.REFRESH_RATE_HZ

    def angle_to_pulse_width(self, angle_deg):
        return self.MIN_ANGLE_PULSE_WIDTH_US + (angle_deg - self.MIN_ANGLE_DEG)*((self.MAX_ANGLE_PULSE_WIDTH_US - self.MIN_ANGLE_PULSE_WIDTH_US)/(self.MAX_ANGLE_DEG - self.MIN_ANGLE_DEG))

    def angle_to_duty(self, angle_deg):
        return self.pulse_width_to_duty(self.angle_to_pulse_width(angle_deg))    

    def update_flap_angle_array(self):
        time_array = np.arange(1/self.flap_sample_rate_hz, 1/self.flap_freq_hz + 1/self.flap_sample_rate_hz, 1/self.flap_sample_rate_hz)
        self.flap_angle_array = self.flap_amplitude_deg*np.sin(2*np.pi*self.flap_freq_hz*time_array)

    def set_flap_freq_hz(self, flap_freq_hz):
        if (flap_freq_hz < self.MIN_FLAP_FREQ_HZ) or (flap_freq_hz > self.MAX_FLAP_FREQ_HZ):
            return 'Invalid flapping frequency!'
        else:
            try:
                self.flap_freq_hz = flap_freq_hz
                self.update_flap_angle_array()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def set_flap_amplitude_deg(self, flap_amplitude_deg):
        if (flap_amplitude_deg < self.MIN_ANGLE_DEG) or (flap_amplitude_deg > self.MAX_ANGLE_DEG):
            return 'Invalid flapping amplitude!'
        else:
            try:
                self.flap_amplitude_deg = flap_amplitude_deg
                self.update_flap_angle_array()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def set_flap_sample_rate_hz(self, flap_sample_rate_hz):
        if (flap_sample_rate_hz < self.MIN_FLAP_SAMPLE_RATE_HZ) or (flap_sample_rate_hz > self.MAX_FLAP_SAMPLE_RATE_HZ):
            return 'Invalid sample rate!'
        else:        
            try:
                self.flap_sample_rate_hz = flap_sample_rate_hz
                self.update_flap_angle_array()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def set_angle_deg(self, angle_deg):
        if (angle_deg < self.MIN_ANGLE_DEG) or (angle_deg > self.MAX_ANGLE_DEG):
            return 'Invalid angle!'
        else:
            try:
                self.pwm.change_duty_cycle(self.angle_to_duty(angle_deg))
                self.angle_deg = angle_deg
                return 'Success!'
            except:
                return 'Error Occurred!'

    def zero_angle(self):
        return self.set_angle_deg(0)

    def stop(self):
        try:
            self.pwm.change_duty_cycle(0)
            self.angle_deg = None
            return 'Success!'
        except: 
            return 'Error Occurred!'