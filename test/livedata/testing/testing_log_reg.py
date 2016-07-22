
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import csv
import random
import datetime
import numpy as np
import math
import skfuzzy as fuzz
import os
os.path.abspath("C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\csvfiles")


ser = serial.Serial(port='COM10',baudrate=9600,timeout=None)
print("connected to: " + ser.portstr)


index = 0;
while True:
    c = ser.readline()
    c = (str(c)[2:-5])
    c = c.split(",")
    try:
        a = [float(i) for i in c]
        print(a)
    except ValueError:
        print([0,0,0,0])