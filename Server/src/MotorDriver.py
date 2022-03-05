from rpi_hardware_pwm import HardwarePWM
import numpy as np
import time

class Motor:

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

        #self.flapThread = None

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
                return str(self.angleDegToDuty(angleDeg)) 
                #return 'Error Occurred!'

    def zeroMotor(self):
        return self.setAngleDeg(0)

    def stopMotor(self):
        try:
            self.pwm.change_duty_cycle(0)
            return 'Success!'
        except: 
            return 'Error Occurred!'

    def runFlapThread(self, flaps):
        try:
            for _ in range(flaps):
                for angle in self.flapAngleArray:
                    timeStart = time.time()
                    self.setAngleDeg(angle)
                    time.sleep((1/self.flapSampleRateHz) - (time.time() - timeStart))
            return 'Success!'
        except: 
            return 'Error Occurred!'
        