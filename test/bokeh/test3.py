import time
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show


# prepare output to server
output_server("test2")

p = figure(plot_width=800, plot_height=400)
p.line([0,1,2,3,4], [0,2,3,4,5], name='ex_line1')
p.line([1,6,5,4,3], [1,1,2,4,2], name= 'ex_line2')
show(p)

# create some simple animation..
# first get our figure example data source
renderer1 = p.select(dict(name="ex_line1"))
ds1 = renderer1[0].data_source
renderer2 = p.select(dict(name="ex_line2"))
ds2 = renderer2[0].data_source

while True:
    # Update y data of the source object
    shuffle(ds1.data["y"])
    shuffle(ds2.data["y"])

    # store the updated source on the server
    cursession().store_objects(ds)
    time.sleep(0.01)