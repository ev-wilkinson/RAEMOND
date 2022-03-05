# RAEMOND

RAEMOND is a manta-ray inspired robot built for Capstone 2021-2022 at the Schulich School of Engineering in University of Calgary.
This repository contains the Python application to control RAEMOND.

Notes:
Client (Windows) connects to server (Raspberry Pi) via bluetooth sockets. Devices must be paired prior to running code.
SSH used for code development and debugging.


## Server

Server directory ran on Raspberry Pi. Includes RAEMOND source files and data captured during swimming experiments.
Compatible with Python 3.

### Dependencies

Use the package manager pip to install the following packages.

```bash
pip install rpi_hardware_pwm
```

### Additional Steps

To run main.py on startup:

1. Edit rc.local
```bash
sudo nano /etc/rc.local
```
2. Add line
```bash
sudo python3 /home/pi/RAEMOND/server/src/main.py &
```
3. Reboot.

To pair bluetooth device:

1. Run bluetoothctl
```bash
bluetoothctl
power on
discoverable on
```
2. On client device find raspberrypi in available bluetooth devices and attempt to pair.

3. Accept connection on Raspberry Pi.

To get MAC address of Raspberry Pi bluetooth:

```bash
hciconfig
```

(update MAC address in main.py)

To configure PWM channels:

1. Edit config.txt

```bash
sudo nano /boot/config.txt
```

2. Add line

```bash
dtoverlay=pwm-2chan,pin=12,func=4,pin2=19,func2=4
```

3. Reboot.


## Client

Client directory is to be used by devices to connect to the server (Raspberry Pi). 
Compatible with Python 3.