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

    # elevator settings
    global LEFT_ELEV_ZERO_OFFSET, RIGHT_ELEV_ZERO_OFFSET, ELEV_CORR_ANGLE_DEG_MAX, ELEV_CORR_ANGLE_DEG_MIN, ELEV_CORR_PERIOD_S, ELEV_CORR_ANGLE_FACTOR
    LEFT_ELEV_ZERO_OFFSET = -35
    RIGHT_ELEV_ZERO_OFFSET = -20
    ELEV_CORR_ANGLE_DEG_MAX = 45
    ELEV_CORR_ANGLE_DEG_MIN = -45
    ELEV_CORR_PERIOD_S = 0.1
    ELEV_CORR_ANGLE_FACTOR = 5