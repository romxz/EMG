import time
import random
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show, Session


session = Session(root_url='http://127.0.0.1:5006/', load_from_config=False)
#session.register('anon3', '1234')
session.login('anon', '1234')
# prepare output to server
output_server("animated_line")
a = random.random()*10
b = random.random()*10
p = figure(plot_width=1000, plot_height=600)
p.xaxis.bounds = (1,100)
p.line([0], [a], name='ex_line1')
p.line([0], [b], name='ex_line2')
show(p)

# create some simple animation..
# first get our figure example data source
renderer1 = p.select(dict(name="ex_line1"))
ds1 = renderer1[0].data_source
renderer2 = p.select(dict(name="ex_line2"))
ds2 = renderer2[0].data_source

i = 0
while True:
    # Update y data of the source object
    a1 = random.random()*10
    b1 = random.random()*10
    ds1.data["x"].append(i)
    ds2.data["x"].append(i)
    ds1.data["y"].append(a1)
    ds2.data["y"].append(b1)
    p.xaxis.bounds = (i-10, i+10)
    p.xaxis.bounds = (i-10, i+10)

    # store the updated source on the server
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0)
    i+= 1