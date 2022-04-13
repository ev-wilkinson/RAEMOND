# settings.py
# Description: holds global settings used throughout program
# Author: Evan Wilkinson

def init():

    # application variables
    global flap_mode
    flap_mode = False

    # bluetooth settings
    global SERVER_MAC_ADRRESS, SERVER_PORT, SERVER_BACKLOG, BT_TIMEOUT_S, BT_BUFFER_SIZE
    SERVER_MAC_ADRRESS = 'B8:27:EB:C3:F3:BC' # MAC address of server (raspberry pi)
    SERVER_PORT = 2 # arbitrary but has to match client
    SERVER_BACKLOG = 1 # specifies number of unaccepted connections that the system will allow before refusing new connections
    BT_TIMEOUT_S = 0.5 # timeout for connection to the client
    BT_BUFFER_SIZE = 1024 # buffer size

    # gpio settings
    global BUTTON_BOUNCE_TIME_MS
    BUTTON_BOUNCE_TIME_MS = 200 # button debouncing delay

    # motor settings
    global MOTOR_FLAP_SAMPLE_RATE_HZ, MOTOR_FLAP_SAMPLE_RATE_HZ_MAX, MOTOR_FLAP_SAMPLE_RATE_HZ_MIN, MOTOR_FLAP_FREQ_HZ_MAX, MOTOR_FLAP_FREQ_HZ_MIN
    MOTOR_FLAP_SAMPLE_RATE_HZ = 20
    MOTOR_FLAP_SAMPLE_RATE_HZ_MAX = 200
    MOTOR_FLAP_SAMPLE_RATE_HZ_MIN = 0
    MOTOR_FLAP_FREQ_HZ_MAX = 2
    MOTOR_FLAP_FREQ_HZ_MIN = 0

    # adc settings
    global ADC_SAMPLE_RATE_HZ, LEFT_POT_CORR_SLOPE, LEFT_POT_CORR_OFFSET, RIGHT_POT_CORR_SLOPE, RIGHT_POT_CORR_OFFSET, LOW_BATTERY_VOLTAGE
    ADC_SAMPLE_RATE_HZ = 20
    LEFT_POT_CORR_SLOPE = -103.45 # (angle2 - angle1)/(Vadc2 - Vadc1) = (90 - 0)/(2.52 - 1.65V)
    LEFT_POT_CORR_OFFSET = -170.7 # -1*SLOPE*Vadc(angle=0) = -(103.45)(1.65V)
    RIGHT_POT_CORR_SLOPE = 103.45 # (angle2 - angle1)/(Vadc2 - Vadc1) = (90 - 0)/(2.52 - 1.65V)
    RIGHT_POT_CORR_OFFSET = -170.7 # -1*SLOPE*Vadc(angle=0) = -(103.45)(1.65V)
    LOW_BATTERY_VOLTAGE = 7.4

    # imu settings
    global IMU_SAMPLE_RATE_HZ, IMU_ACC_SENSITIVITY_FACTOR, IMU_GYRO_SENSITIVITY_FACTOR, IMU_PITCH_OFFSET, IMU_ROLL_OFFSET
    IMU_SAMPLE_RATE_HZ = 20
    IMU_ACC_SENSITIVITY_FACTOR = 16384.0
    IMU_GYRO_SENSITIVITY_FACTOR = 131.0
    IMU_PITCH_OFFSET = -5.2 # calibrated when device is on flat surface
    IMU_ROLL_OFFSET = -1.0 # calibrated when device is on flat surface

    # elevator settings
    global LEFT_ELEV_ZERO_OFFSET, RIGHT_ELEV_ZERO_OFFSET, ELEV_CORR_ANGLE_DEG_MAX, ELEV_CORR_ANGLE_DEG_MIN, ELEV_CORR_PERIOD_S, ELEV_CORR_ANGLE_FACTOR
    LEFT_ELEV_ZERO_OFFSET = -35 # calibrated servo zero value after installation
    RIGHT_ELEV_ZERO_OFFSET = -20 # calibrated servo zero value after installation
    ELEV_CORR_ANGLE_DEG_MAX = 45 # max elevator set angle
    ELEV_CORR_ANGLE_DEG_MIN = -45 # min elevator set angle
    ELEV_CORR_PERIOD_S = 0.1
    ELEV_CORR_ANGLE_FACTOR = 2 # gain on imu sensor feedback

    # data log settings
    global LOG_SAMPLE_RATE_HZ
    LOG_SAMPLE_RATE_HZ = 20