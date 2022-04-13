# RAEMOND

RAEMOND is a manta-ray inspired robot built for Capstone 2021-2022 at the Schulich School of Engineering in University of Calgary.
This repository contains the Python application to control RAEMOND.

Notes:
Server directory ran on Raspberry Pi Zero. Includes RAEMOND source files and data captured during swimming experiments.
Client directory compatible. Sends commands to server via bluetooth sockets. Devices must be paired prior to running server and client.
SSH used to control Raspberry Pi Zero. See https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html
Alternatively if server and client are already paired then main.py can be ran on Raspberry Pi start-up (see below).

## Folder Structure

```
RAEMOND
├── Client
│   └── run.py
├── Server
│   ├── data
│   └── src
│       └── adc.py
│       └── commands.py
│       └── data_log.py
│       └── elevator.py
│       └── gpio.py
│       └── imu.py
│       └── main.py
│       └── motor.py
│       └── settings.py
└── README.md
```

## Dependencies

Use the package manager pip to install the following packages.

```bash
pip install spidev
pip install smbus
pip install rpi_hardware_pwm
```

## Additional Steps

To pair bluetooth device:

1. Run bluetoothctl
```bash
bluetoothctl
power on
discoverable on
```
2. On client device find raspberrypi in available bluetooth devices and attempt to pair.

3. Accept connection on Raspberry Pi.

To get MAC address of Raspberry Pi bluetooth (update MAC address in settings.py):

```bash
hciconfig
```

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

To run application:

1. On Raspberry Pi
```bash
cd RAEMOND/Server/src/
python3 main.py
```
2. On Windows PC
```bash
cd RAEMOND/Client/
python3 run.py
```

To run main.py on Raspberry Pi startup:

1. Edit rc.local
```bash
sudo nano /etc/rc.local
```
2. Add line
```bash
sudo python3 /home/pi/RAEMOND/Server/src/main.py &
```
3. Reboot.