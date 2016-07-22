import serial
import matplotlib.pyplot as plt

ser = serial.Serial(port='COM10',baudrate=9600,timeout=None)

while True:
    ser.reset_input_buffer()
    
    c = ser.readline()
    print(c)