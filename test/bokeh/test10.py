import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models.sources import ColumnDataSource
from bokeh.client import push_session
from bokeh.driving import linear
import random
from random import shuffle
from bokeh.plotting import figure, output_server,  show
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform
from datetime import date
from random import randint

 
antialias = 10
N = 10

data = {"val1":[], "val2":[]}
source = ColumnDataSource(data)
columns = [
        TableColumn(field="val1", title="val1"),
        TableColumn(field="val2", title="val2"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=280)


 
@linear(m=0.5, b=0) #step will increment by 0.05 every time
def update(step):
    data["val1"].append(random.random())
    data["val2"].append(random.random())
    
 
# open a session to keep our local document in sync with server
session = push_session(curdoc())
curdoc().add_periodic_callback(update, 10) #period in ms
session.show()
session.loop_until_closed()