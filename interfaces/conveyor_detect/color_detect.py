import cv2
import serial
import numpy as np
from utils import *

PORT = "/dev/ttyAMC0"
BAUDRATE = 9600
CAMERA = 0
ser_flag = False
try:
    ser = serial.Serial(port=PORT, baudrate=BAUDRATE)
except:
    print("Choice another port:")
    find_ports()
    iPort = str(input("Type the port name: "))
    try:
        ser = serial.Serial(port=iPort, baudrate=BAUDRATE)
        if ser.is_open:
            ser_flag = True

    except:
        print("Port not found")
        ser_flag = False

if ser_flag:
    print("Python Code")
else:
    print("Bye Bye")
