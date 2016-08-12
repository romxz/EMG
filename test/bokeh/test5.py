# FOR SERVER SETUP : bokeh-server -m --ip 127.0.0.1

from bokeh.plotting import hplot, figure, show, output_server, Session
from numpy import arange, sin, cos


session = Session(root_url='http://127.0.0.1:5006/', load_from_config=False)
#session.register('anon3', '1234')
session.login('anon', '1234')




output_server('test')


x = arange(0, 10, .1)
y1 = sin(x)
y2 = cos(x)
fig1 = figure(title='sin', plot_width=500, plot_height=200)
fig1.line(x, y1)
fig2 = figure(title='cos', plot_width=500, plot_height=200)
fig2.line(x, y2)
plot = hplot(fig1, fig2)

show(plot)
