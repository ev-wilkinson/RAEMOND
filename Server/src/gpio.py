import RPi.GPIO as GPIO
import threading
import time
import settings

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global IOCtrl, BlueLEDBlinker
    IOCtrl = IOUtils()
    BlueLEDBlinker = BlueLEDBlinkingThread()
    BlueLEDBlinker.start()

def button_pressed(channel):
    if settings.flap_mode:
        settings.flap_mode = False
    else:
        settings.flap_mode = True

class BlueLEDBlinkingThread(threading.Thread):
    def __init__(self):
        super(BlueLEDBlinkingThread, self).__init__()
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.blink_interval_s = 1

    def run(self):
        global IOCtrl
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            while True:
                if self.paused:
                    break
                IOCtrl.turn_off_blue()
                time.sleep(self.blink_interval_s)
                IOCtrl.turn_on_blue()
                time.sleep(self.blink_interval_s)

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def set_blinking_interval(self, blink_interval_s):
        self.blink_interval_s = blink_interval_s
        

class IOUtils:

    BLUE_LED_PIN = 14
    RED_LED_PIN = 15
    BUTTON_PIN = 27

    def __init__(self):

        # setup button 
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=settings.BUTTON_BOUNCE_TIME_MS)

        # setup leds
        GPIO.setup(self.BLUE_LED_PIN, GPIO.OUT)
        GPIO.output(self.BLUE_LED_PIN, GPIO.LOW)
        GPIO.setup(self.RED_LED_PIN, GPIO.OUT)
        self.turn_off_red()

    def turn_on_red(self):
        GPIO.output(self.RED_LED_PIN, GPIO.HIGH)

    def turn_off_red(self):
        GPIO.output(self.RED_LED_PIN, GPIO.LOW)

    def turn_on_blue(self):
        GPIO.output(self.BLUE_LED_PIN, GPIO.HIGH)

    def turn_off_blue(self):
        GPIO.output(self.BLUE_LED_PIN, GPIO.LOW)
