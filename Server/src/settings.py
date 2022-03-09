def init():

    # bluetooth settings
    global SERVER_MAC_ADRRESS, SERVER_PORT, SERVER_BACKLOG, BUFFER_SIZE
    SERVER_MAC_ADRRESS = 'B8:27:EB:C3:F3:BC' # MAC address of server (raspberry pi)
    SERVER_PORT = 2 # arbitrary but has to match client
    SERVER_BACKLOG = 1 # specifies number of unaccepted connections that the system will allow before refusing new connections
    BUFFER_SIZE = 1024 # buffer size