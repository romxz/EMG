# FOR SERVER SETUP : bokeh-server -m --ip 127.0.0.1
import time
import random
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show, Session
import serial


ser = serial.Serial(port='COM5',baudrate=9600,timeout=None)
print("connected to: " + ser.portstr)
session = Session(root_url='http://127.0.0.1:5006/', load_from_config=False)
#session.register('anon3', '1234')
session.login('anon', '1234')

output_server("animated_line2")
a = random.random()*10
b = random.random()*10
p = figure(plot_width=1000, plot_height=600)
p.xaxis.bounds = (1,100)

p.line([], [], name='ex_line1', color = "blue")
p.line([], [], name='ex_line2', color = "red")
show(p)

renderer1 = p.select(dict(name="ex_line1"))
ds1 = renderer1[0].data_source
renderer2 = p.select(dict(name="ex_line2"))
ds2 = renderer2[0].data_source

    
i = 0
while True:
    c = ser.readline()
    c = (str(c)[2:-5])
    c = c.split(",")
    a = [float(i) for i in c]
    #a = [0.1,0.2]
    print(a)
    a1 = a[0]
    b1 = a[0] 
    if i<=30:
        ds1.data["x"].append(i)
        ds2.data["x"].append(i)
        ds1.data["y"].append(a1)
        ds2.data["y"].append(b1)
        i+= 1
    if i>30:
        for j in range(len(ds1.data["y"])-1):
            ds1.data["y"][j] = ds1.data["y"][j+1]
            ds2.data["y"][j] = ds2.data["y"][j+1]
        ds1.data["y"][-1] = a1
        ds2.data["y"][-1] = b1
        i+= 1
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0.02)
    
    
