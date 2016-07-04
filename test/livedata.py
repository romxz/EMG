import serial
import matplotlib.pyplot as plt

ser = serial.Serial(port='COM10',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

print("connected to: " + ser.portstr)

#this will store the line
line = []
vallist = []
val_a = []
val_b = []

while True:
    index = 0
    for c in ser.readline():
        if not(c == 13):
            line.append(chr(c)) 
        if (c == 13):
            a = ("".join(str(x) for x in line))
            a = a.replace("\n", ",")
            a = a.split(",")
        if index%2 == 0:
            val_a.append(a[index])
        elif index%2 == 1:
            val_b.append(a[index])
        plt.scatter(val_a[i], val_b[i])
        i += 1
        #insert the timing
        plt.pause(1)
        print(val_a)

while True:
    #insert the timing
    plt.pause(1)