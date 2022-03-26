import spidev
import threading
import time

def init():
    global ADCData, ADCCtrl
    ADCData = ADCUtils()
    ADCCtrl = ADCThread()
    ADCCtrl.start()

class ADCThread(threading.Thread):
    def __init__(self):
        super(ADCThread, self).__init__()
        self.paused = False  # Start out running.
        self.state = threading.Condition()
        self.sample_rate_hz = 20

    def run(self):
        global ADCData
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            while True:
                if self.paused:
                    break
                time_start = time.time()
                ADCData.get_all_data()
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

class ADCUtils:

    # SPI constants
    SPI_BUS = 0
    SPI_DEVICE = 0
    SPI_MODE = 0b01
    SPI_SPEED_HZ = 122000

    # ADC constants
    ADC_VREF = 3.3
    ADC_FULLSCALE = 4096
    ADC_START_BIT = 0b1
    ADC_SINGLE_ENDED = 0b1
    ADC_CH0 = 0b000
    ADC_CH1 = 0b001
    ADC_CH2 = 0b010
    ADC_CH3 = 0b011
    ADC_CH4 = 0b100
    ADC_CH5 = 0b101
    ADC_CH6 = 0b110
    ADC_CH7 = 0b111
    ADC_DONT_CARE_BIT = 0b0
    ADC_DONT_CARE_BYTE = 0x00

    # current sense amplifier constants
    SENSE_RES = 0.003
    SENSE_GAIN = 50

    # voltage divider constants
    VOLT_DIV_FACTOR_7V4 = 100/300
    VOLT_DIV_FACTOR_5V = 300/500

    # potentiometer corrections
    LEFT_POT_SLOPE = 103.45 # (angle2 - angle1)/(Vadc2 - Vadc1) = (90 - 0)/(2.52 - 1.65V)
    LEFT_POT_OFFSET = -170.69 # -1*SLOPE*Vadc(angle=0) = -(103.45)(1.65V)
    RIGHT_POT_SLOPE = 103.45 # (angle2 - angle1)/(Vadc2 - Vadc1) = (90 - 0)/(2.52 - 1.65V)
    RIGHT_POT_OFFSET = -170.69 # -1*SLOPE*Vadc(angle=0) = -(103.45)(1.65V)


    def __init__(self):

        # initialize spi communication
        self.spi = None
        self.spi_init()

        # setup variables
        self.adc_ch0_raw = None
        self.adc_ch1_raw = None
        self.adc_ch2_raw = None
        self.adc_ch3_raw = None
        self.adc_ch4_raw = None
        self.adc_7V4_current = None
        self.adc_7V4_voltage = None
        self.adc_5V_voltage = None
        self.adc_left_angle = None
        self.adc_right_angle = None

        # initial data aquisition
        self.get_all_data()

    def spi_init(self):
        self.spi = spidev.SpiDev()
        self.spi.open(self.SPI_BUS, self.SPI_DEVICE)
        self.spi.max_speed_hz = self.SPI_SPEED_HZ
        self.spi.mode = self.SPI_MODE

    def spi_xfer_bytes(self, byte_array):
        return self.spi.xfer(byte_array)

    def get_adc_bytes(self, channel_bits):
        send_bits = (self.ADC_START_BIT << 18) + (self.ADC_SINGLE_ENDED << 17) + (channel_bits << 14) 
        return self.spi_xfer_bytes(send_bits.to_bytes(3, byteorder='big'))

    def get_adc_voltage(self, channel_bits):
        return self.ADC_VREF*int.from_bytes(self.get_adc_bytes(channel_bits), byteorder='big')/self.ADC_FULLSCALE

    def get_7V4_current(self):
        adc_voltage = self.get_adc_voltage(self.ADC_CH0)
        self.adc_ch0_raw = adc_voltage
        self.adc_7V4_current = adc_voltage/self.SENSE_RES/self.SENSE_GAIN

    def get_7V4_voltage(self):
        adc_voltage = self.get_adc_voltage(self.ADC_CH1)
        self.adc_ch1_raw = adc_voltage
        self.adc_7V4_voltage = adc_voltage/self.VOLT_DIV_FACTOR_7V4

    def get_5V_voltage(self):
        adc_voltage = self.get_adc_voltage(self.ADC_CH2)
        self.adc_ch2_raw = adc_voltage
        self.adc_5V_voltage = adc_voltage/self.VOLT_DIV_FACTOR_5V

    def get_left_angle(self):
        adc_voltage = self.get_adc_voltage(self.ADC_CH3)
        self.adc_ch3_raw = adc_voltage
        self.adc_left_angle = adc_voltage*self.LEFT_POT_SLOPE + self.LEFT_POT_OFFSET

    def get_right_angle(self):
        adc_voltage = self.get_adc_voltage(self.ADC_CH4)
        self.adc_ch4_raw = adc_voltage        
        self.adc_right_angle = adc_voltage*self.RIGHT_POT_SLOPE + self.RIGHT_POT_OFFSET

    def get_all_data(self):
        self.get_7V4_current()
        self.get_7V4_voltage()
        self.get_5V_voltage()
        self.get_left_angle()
        self.get_right_angle()