import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models.sources import ColumnDataSource
from bokeh.client import push_session
from bokeh.driving import linear
import random
 
antialias = 10
N = 10
x = np.linspace(0, N, N*antialias)
y1 = np.sin(x)
y2 = np.cos(x)
 
myfigure = figure(plot_width=800, plot_height=400)
datacoords = ColumnDataSource(data=dict(x=x, y1=y1, y2=y2))
linea = myfigure.line("x", "y1", source=datacoords, color = "red")
lineb = myfigure.line("x", "y2", source=datacoords, color = "blue")

 
@linear(m=0.5, b=0) #step will increment by 0.05 every time
def update(step):
    new_x = np.linspace(step, N+step, N*antialias)
    new_y1 = np.sin(new_x)
    new_y2 = np.cos(new_x)
    test1 = []
    test2 = []
    for i in range(len(new_x)):
        test1.append(random.random())
        test2.append(random.random())
    
    linea.data_source.data["x"] = new_x
    linea.data_source.data["y1"] = test1
    lineb.data_source.data["y2"] = test2
 
# open a session to keep our local document in sync with server
session = push_session(curdoc())
curdoc().add_periodic_callback(update, 10) #period in ms
session.show()
session.loop_until_closed()