import time
import random
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show, Session


session = Session(root_url='http://127.0.0.1:5006/', load_from_config=False)
#session.register('anon3', '1234')
session.login('anon', '1234')

output_server("animated_line")
a = random.random()*10
b = random.random()*10
p = figure(plot_width=1000, plot_height=600)
p.xaxis.bounds = (1,100)


p.multi_line([[0], [a]], [[0], [b]],
             color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)
show(p)

renderer1 = p.select(dict(p))
ds = renderer1[0].data_source

i = 0
while True:
    a1 = random.random()*10
    b1 = random.random()*10
    ds1.data["x"].append(i)
    ds2.data["x"].append(i)
    ds1.data["y"].append(a1)
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0)
    i+= 1