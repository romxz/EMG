<<<<<<< HEAD

=======
<<<<<<< HEAD
<<<<<<< HEAD
# FOR SERVER SETUP : bokeh-server -m --ip 127.0.0.1
=======
>>>>>>> 668ffd5a81a765d02feed26e209efce573d06d30
=======
>>>>>>> 668ffd5a81a765d02feed26e209efce573d06d30
>>>>>>> 99db9b5f6b51fd0463277c2f941d63cc0055d91f
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

p.line([0], [a], name='ex_line1', color = "blue")
p.line([0], [b], name='ex_line2', color = "red")
show(p)

renderer1 = p.select(dict(name="ex_line1"))
ds1 = renderer1[0].data_source
renderer2 = p.select(dict(name="ex_line2"))
ds2 = renderer2[0].data_source

i = 0
while True:
    a1 = random.random()*10
    b1 = random.random()*10
    ds1.data["x"].append(i)
    ds2.data["x"].append(i)
    ds1.data["y"].append(a1)
    ds2.data["y"].append(b1)
<<<<<<< HEAD

=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 99db9b5f6b51fd0463277c2f941d63cc0055d91f
    p.line(ds1.data["x"], ds1.data["y"], legend = "hi", name='ex_line1', color = "blue")
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0)
    i+= 1
    
<<<<<<< HEAD
=======
=======
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0)
    i+= 1
>>>>>>> 668ffd5a81a765d02feed26e209efce573d06d30
=======
    cursession().store_objects(ds1)
    cursession().store_objects(ds2)
    time.sleep(0)
    i+= 1
>>>>>>> 668ffd5a81a765d02feed26e209efce573d06d30
>>>>>>> 99db9b5f6b51fd0463277c2f941d63cc0055d91f
