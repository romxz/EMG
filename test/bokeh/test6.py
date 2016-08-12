import time
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show

# prepare output to server
output_server("animation")

x = [1,2,3,4,5]
y = [1,2,3,4,5]

p = figure(plot_width=400, plot_height=400)
p.circle(x, y, name='ex_circle', size=25)
show(p)

# create some simple animation..
# first get our figure example data source
renderer = p.select(dict(name="ex_circle"))
ds = renderer[0].data_source

while True: # Update y data of the source object 
    shuffle(ds.data["y"]) # store the updated source on the server                         
    cursession().store_objects(ds) 
    time.sleep(0.5)