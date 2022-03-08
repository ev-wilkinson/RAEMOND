from rpi_hardware_pwm import HardwarePWM
import threading
import numpy as np
import time

def init():

    # initiliaze motors
    global RMotor, LMotor
    RMotor, LMotor = Motor(pwm_channel=0), Motor(pwm_channel=1)
    RMotor.start()
    LMotor.start()

class Motor(threading.Thread):
    def __init__(self, pwm_channel):
        super(Motor, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.motorUtils = MotorUtils(pwm_channel)

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            for angle in self.motorUtils.flapAngleArray:
                if self.paused:
                    break
                timeStart = time.time()
                self.motorUtils.setAngleDeg(angle)
                time.sleep((1/self.motorUtils.flapSampleRateHz) - (time.time() - timeStart))

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

class MotorUtils:

    # motor constants
    refreshRateHz = 333

    # limit values
    maxAngleDeg = 65
    minAngleDeg = -65
    maxAnglePulseWidthUs = 2100
    minAnglePulseWidthUs = 900
    maxFlapFreqHz = 2
    minFlapFreqHz = 0
    maxflapSampleRateHz = 200
    minflapSampleRateHz = 0

    def __init__(self, pwm_channel):

        self.flapFreqHz = 0.25
        #self.flapDelaySec = 0
        self.flapAmplitudeDeg = 30
        self.flapSampleRateHz = 50
        self.flapAngleArray = None
        self.updateFlapAngleArray()

        self.pwm = HardwarePWM(pwm_channel=pwm_channel, hz=self.refreshRateHz)
        self.pwm.start(0) # initialize pwm at 0% duty

    def pulseWidthUsToDuty(self, pulseWidthUs):
        return 100*pulseWidthUs*1e-6*self.refreshRateHz

    def angleDegToPulseWidthUs(self, angleDeg):
        return self.minAnglePulseWidthUs + (angleDeg - self.minAngleDeg)*((self.maxAnglePulseWidthUs - self.minAnglePulseWidthUs)/(self.maxAngleDeg - self.minAngleDeg))

    def angleDegToDuty(self, angleDeg):
        return self.pulseWidthUsToDuty(self.angleDegToPulseWidthUs(angleDeg))    

    def updateFlapAngleArray(self):
        timeArray = np.arange(1/self.flapSampleRateHz, 1/self.flapFreqHz + 1/self.flapSampleRateHz, 1/self.flapSampleRateHz)
        self.flapAngleArray = self.flapAmplitudeDeg*np.sin(2*np.pi*self.flapFreqHz*timeArray)

    def setFlapFreqHz(self, flapFreqHz):
        if (flapFreqHz < self.minFlapFreqHz) or (flapFreqHz > self.maxFlapFreqHz):
            return 'Invalid flapping frequency!'
        else:
            try:
                self.flapFreqHz = flapFreqHz
                self.updateFlapAngleArray()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def setFlapAmplitudeDeg(self, flapAmplitudeDeg):
        if (flapAmplitudeDeg < self.minAngleDeg) or (flapAmplitudeDeg > self.maxAngleDeg):
            return 'Invalid flapping amplitude!'
        else:
            try:
                self.flapAmplitudeDeg = flapAmplitudeDeg
                self.updateFlapAngleArray()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def setFlapSampleRateHz(self, flapSampleRateHz):
        if (flapSampleRateHz < self.minflapSampleRateHz) or (flapSampleRateHz > self.maxflapSampleRateHz):
            return 'Invalid sample rate!'
        else:        
            try:
                self.flapSampleRateHz = flapSampleRateHz
                self.updateFlapAngleArray()
                return 'Success!'
            except:
                return 'Error Occurred!'

    def setAngleDeg(self, angleDeg):
        if (angleDeg < self.minAngleDeg) or (angleDeg > self.maxAngleDeg):
            return 'Invalid angle!'
        else:
            try:
                self.pwm.change_duty_cycle(self.angleDegToDuty(angleDeg))
                return 'Success!'
            except:
                return 'Error Occurred!'

    def zeroMotor(self):
        return self.setAngleDeg(0)

    def stopMotor(self):
        try:
            self.pwm.change_duty_cycle(0)
            return 'Success!'
        except: 
            return 'Error Occurred!'