import json
import serial 
import time

data = {}
ser = serial.Serial(port='COM6',baudrate=9600,timeout=None)

newpath = ('C:\\Users\\Michael\\Documents\\GitHub\\EMG\\test\\webbrowser\\test.jsonp') 
while True:
    a = str(ser.readline())
    data['key'] = a[2:-5]
    json_data = json.dumps(data)
    print ('JSON: ', json_data)
    with open(newpath, 'w') as fp:
        json.dump(data, fp)
    