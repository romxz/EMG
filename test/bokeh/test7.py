import time
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show

# prepare output to server
output_server("animated_line")

p = figure(plot_width=1000, plot_height=600)
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], name='ex_line1')
p.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 3], name='ex_line2')
show(p)

# create some simple animation..
# first get our figure example data source
renderer1 = p.select(dict(name="ex_line1"))
ds1 = renderer1[0].data_source
renderer2 = p.select(dict(name="ex_line2"))
ds2 = renderer2[0].data_source


while True:
    # Update y data of the source object
    print(ds1.data["x"])
    print(ds1.data["y"])
    shuffle(ds1.data["y"])
    shuffle(ds2.data["y"])

    # store the updated source on the server
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0.5)