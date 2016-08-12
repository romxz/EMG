from bokeh.plotting import figure, output_file, show
import random

# output to static HTML file
output_file("index.html")

p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
index = 1
while index<500:
    a = random.random()
    b = random.random()
    print ([a,b])
    p.circle([a], [b], size=20, color="navy", alpha=0.5)
    index += 1

# show the results
show(p)
