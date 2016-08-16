# FOR SERVER SETUP : bokeh-server -m --ip 127.0.0.1
import time
import random
from random import shuffle
from bokeh.plotting import figure, output_server, cursession, show, Session
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show, vform
from datetime import date
from random import randint


#session = Session(root_url='http://127.0.0.1:5006/', load_from_config=False)
#session.register('anon3', '1234')
#session.login('anon', '1234')

# output_server("animated_line2")
# a = random.random()*10
# b = random.random()*10
# p = figure(plot_width=1000, plot_height=600)
# p.xaxis.bounds = (1,100)
# 
# p.line([], [], name='ex_line1', color = "blue")
# p.line([], [], name='ex_line2', color = "red")
# show(p)
# 
# renderer1 = p.select(dict(name="ex_line1"))
# ds1 = renderer1[0].data_source
# renderer2 = p.select(dict(name="ex_line2"))
# ds2 = renderer2[0].data_source


output_server("data_table.html")

data = {"val1":[], "val2":[]}
source = ColumnDataSource(data)
columns = [
        TableColumn(field="val1", title="val1"),
        TableColumn(field="val2", title="val2"),
    ]
data_table = DataTable(source=source, columns=columns, width=400, height=280)

index = 0
while index<5:
    a = random.random()
    b = random.random()
    data["val1"].append(a)
    data["val2"].append(b)
    index += 1


   
# i = 0
# while True:
#     a1 = random.random()*10
#     b1 = random.random()*10
#     if i<=30:
#         ds1.data["x"].append(i)
#         ds2.data["x"].append(i)
#         ds1.data["y"].append(a1)
#         ds2.data["y"].append(b1)
#         i+= 1
#     if i>30:
#         for j in range(len(ds1.data["y"])-1):
#             ds1.data["y"][j] = ds1.data["y"][j+1]
#             ds2.data["y"][j] = ds2.data["y"][j+1]
#         ds1.data["y"][-1] = a1
#         ds2.data["y"][-1] = b1
#         i+= 1
#     cursession().store_objects(ds1)
#     cursession().store_objects(ds2)
#     time.sleep(0.02)



