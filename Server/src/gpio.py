import RPi.GPIO as GPIO
import threading
import time

def init():
    global button_enabled, BlueLEDBlinker, IOCtrl
    button_enabled = False
    IOCtrl = IOUtils()
    BlueLEDBlinker = BlueLEDBlinkingThread()
    BlueLEDBlinker.start()

def button_pressed(channel):
    global button_enabled
    if button_enabled:
        button_enabled = False
    else:
        button_enabled = True
    print(f'Button enabled: {button_enabled}')

class BlueLEDBlinkingThread(threading.Thread):
    def __init__(self):
        super(BlueLEDBlinkingThread, self).__init__()
        self.paused = False  # Start out running.
        self.state = threading.Condition()

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
                time.sleep(0.5)
                IOCtrl.turn_on_blue()
                time.sleep(0.5)

    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

class IOUtils:

    BLUE_LED_PIN = 14
    RED_LED_PIN = 15
    BUTTON_PIN = 27

    def __init__(self):
        
        # gpio settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # setup button 
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=200)

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
