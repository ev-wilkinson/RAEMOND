def init():

    # bluetooth settings
    global serverMACAddress, serverPort, serverBacklog, bufferSize
    serverMACAddress = 'B8:27:EB:C3:F3:BC' # MAC address of server (raspberry pi)
    serverPort = 2 # arbitrary but has to match client
    serverBacklog = 1 # specifies number of unaccepted connections that the system will allow before refusing new connections
    bufferSize = 1024 # buffer size