# Intro to data visualization with Bokeh

## PyData at Strata

- Sarah Bird [@birdsarah](https://twitter.com/birdsarah)
- Bryan Van de Ven [@bryvdv](https://twitter.com/bryvdv)

<small>March 29th, 2016</small>


---

## Overview

- 11:30 - 12:30 Intro to Bokeh  
- 12:30 - 13:30 LUNCH
- 13:30 - 14:30 Hands-on

---


## Bokeh

<img class="slide_image" src="images/gallery-screenshot.png" style="position: absolute; top: 0; right: 0;">

- data visualization
- web-based & interactive
- no javascript required
- large data
- streaming data


---

## Core concepts for today

- Overview of Bokeh's functionality
- Navigating Bokeh's interfaces 
 - charts, plotting, and probably not models!
- Bokeh server 
 - what it is, what it isn't, do I need it
- Sharing your work 
 - notebook, standalone files, server 
- Awareness of the Bokeh ecosystem

---
<img class="slide_image" src="images/box_chart.png" style="position: absolute; top: 0px; right: 0; width: 300px; height: auto">
### Demo 1 - Charts in the notebook
quick & easy data exploration

* work in the notebok
```python
from bokeh.io import output_notebook, show
output_notebook()
```
* make charts - simple one-liners accept tabular data
```python
from bokeh.charts import Bar, BoxPlot, Histogram, Scatter....
Scatter(df, x='mpg', y='hp', color='cyl')
BoxPlot(df, values='mpg', label='cyl', marker='square')
```

<small>
[bokeh.pydata.org/en/latest/docs/user_guide/charts.html](http://bokeh.pydata.org/en/latest/docs/user_guide/charts.html)
</small>

---

<img class="slide_image" src="images/clustering.png" style="position: absolute; top: 0px; right: 0px; width: 300px; height: auto">
### Demo 2 - Server - clustering
interact in the browser, run python code
```python
def update_samples_or_dataset(attrname, old, new):
    dataset = dataset_select.value
    algorithm = algorithm_select.value
    X, y = get_dataset(dataset, n_samples)
    X, y_pred = clustering(X, algorithm, n_clusters)
    new_data = {'x': X[:, 0], 'y': X[:, 1]}
    source.data = new_data
    
algorithm_select = Select(value='MiniBatchKMeans', options=opts)
algorithm_select.on_change('value', update_algorithm_or_clusters)
```

<small>
[github.com/bokeh/bokeh/tree/master/examples/app/clustering](https://github.com/bokeh/bokeh/tree/master/examples/app/clustering)
</small>

---

### Demo 3 - Server - streaming
<img class="slide_image" src="images/ohlc.png" style="position: absolute; top: 0px; right: 0px; width: 400px; height: auto">

* connect your plot to a streaming data source
* bokeh will take care of the rest
    ```python
    def update():
        new_data = get_new_data()
        source.stream(new_data, 300)
        
    doc.add_periodic_callback(update, 50)
    ```
<small>
[github.com/bokeh/bokeh/tree/master/examples/app/ohlc](https://github.com/bokeh/bokeh/tree/master/examples/app/ohlc)
</small>

---

<img class="slide_image" src="images/datashader.png" style="position: absolute; top: 0px; right: 0px; width: 400px; height: auto">
### Demo 4 - Datashader
Plotting **very** large datasets meaningfully

Uses bokeh's interactivity, hooks into <br />
powerful python libraries

[datashader.readthedocs.org](http://datashader.readthedocs.org)

---

## Core concepts for today

- Overview of Bokeh's functionality
- Navigating Bokeh's interfaces 
 - charts, plotting, and probably not models!
- Bokeh server 
 - what it is, what it isn't, do I need it
- Sharing your work 
 - notebook, standalone files, server 
- Awareness of the Bokeh ecosystem

---
Thanks to:

![numfocus](images/NumFocus.png)
---

## Bokeh - Core

- Python-based - http://bokeh.pydata.org
- Charts (Bar chart, Histogram...)
- Custom plots
- User interactions & styling
- Server interactions

---

## Bokeh - Ecosystem

- Other language bindings: rbokeh (actively maintained), scala (activeley maintained), julia (not maintained), typescript (actively maintained)
- Datashader - interact with BIG data
- Write your own custom models

---

## Interfaces

There are a number of ways to use Bokeh - pick the one that's right for you:

* Charts (high speed)
* Plotting (sensible defaults)
* Models (high customization)

We'll come back to this multiple times today.

---

<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.charts` (high speed)</h5>

- One-line charts
- Processes your data & spits out a chart


<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.plotting` (sensible defaults)</h5>

- Tries to pick sensible defaults
- You organize your data, it organizes your plot

<h5 style="padding-top: 1em; margin-bottom: -0.2em"> `bokeh.models` (high customization)</h5>

- The lowest level
- Offers you the most control
- Do all the work yourself

---

# Charts

---

### Charts
* Area, Bar, Box, Donut, Dot, Heatmap, Histogram, Horizon, Line, Scatter,
Step, Timeseries
* Wherever possible, the interface is designed to be simple to use with [pandas](http://pandas.pydata.org), by accepting a DataFrame and names of columns directly to specify data.

[reference](http://bokeh.pydata.org/en/latest/docs/reference/charts.html#module-bokeh.charts)

/notebooks/Charts.ipynb

Note: 
box plot whiskers are: the lowest datum still within 1.5 IQR of the lower quartile, and the highest datum still within 1.5 IQR

---

Inputs:

* categorical: values / label (Bar, Dot)
* continuous: x / y (Scatter, Line)

Defaults:

* plot_width, plot_height, tools, legend, xgrid, ygrid, xlabel, ylabel, xscale, yscale, title_text_font_size, responsive.....

---

### Becoming a charts power user

* Set-up your defaults
* Attributes - cat, color, marker
* Aggregations - sum, mean, count, nunique, median, min, max
* Data operations - blend, stack
* Attribute Specification - `label=['col1','col2']`

---

### Charts resources

* [bokeh.pydata.org/en/latest/docs/user_guide/charts.html](http://bokeh.pydata.org/en/latest/docs/user_guide/charts.html)
* [bokeh.pydata.org/en/latest/docs/reference/charts.html](http://bokeh.pydata.org/en/latest/docs/reference/charts.html)
* [examples/howto/charts/](https://github.com/bokeh/bokeh/tree/master/examples/howto/charts)
* [examples/charts/](https://github.com/bokeh/bokeh/tree/master/examples/charts)

---

At the heart of Bokeh is the `ColumnDataSource`

| 'column of xs' | 'column of ys'
|---|---
|0|1 
|1|2
|3|4

[notebooks/ColumnDataSource.ipynb](http://localhost:8888/notebooks/notebooks/ColumnDataSource.ipynb)


---

# Plotting

---

```python
from bokeh.plotting import figure

p = figure(plot_width=400, plot_height=200, title='plot')
p.circle(x=[1, 2, 3], y=[2, 4, 6])
show(p)

```
<br />
```python
from bokeh.models import ColumnDataSource
source = ColumnDataSource(data_frame)
p = figure(plot_width=400, plot_height=200, title='plot')
p.circle(x='x', y='y', source=source)
show(p)
```
---

```python
from bokeh.models import ColumnDataSource
source = ColumnDataSource(data_frame)
p = figure(plot_width=400, plot_height=200, title='plot')
p.circle(x='x1', y='y1', color='col2', size='col4', source=source)
p.rect(x='x2', y='y2', source=source)
show(p)
```

---

### Sharing ranges & sources

```python
from bokeh.plotting import figure

p = figure(plot_width=400, plot_height=200, title='plot')
p.circle(x=[1, 2, 3], y=[2, 4, 6])
show(p)

```

[User Guide](http://bokeh.pydata.org/en/latest/docs/user_guide/interaction.html#linked-panning)

[Examples - github.com/bokeh/bokeh/tree/0.11.1/examples/plotting](https://github.com/bokeh/bokeh/tree/0.11.1/examples/plotting)

---
### Output

* output_notebook()
* output_file()
* embedding - file_html(), components()

---

### Resources

* `INLINE` - in the file
* `CDN` - load from web
* There are other options

---

# Server

---

## Bokeh Server

* easily connect visualization to python code e.g.
 * drive scikit-learn from data point selection in 10 lines of code
 * perform complex downsampling on pan/zoom
* streaming data
 * update visualizations from external data sources or sensors
 
See live hosted examples here:

http://demo.bokehplots.com

---

# How the server works

![DataShader pipeline](images/server_arch.png)

Reflect Python and JavaScript state automatically and transparently. 

---

Sliders Example Walk-through

* commom imports and data set up

```
import numpy as np

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.models.widgets import Slider, TextInput
from bokeh.io import curdoc

N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))
```

---
Sliders Example Walk-through (cont.)

* set up a plot

```
plot = Figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,resize,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
```

**Note** -- use `Figure` (capital F) if the plot will be part of a larger layout, or `figure` (lower f) if you will just be adding the plot and nothing else. 

---

Sliders Example Walk-through (cont.)

* set up some widgets

```
text = TextInput(title="title", value='my sine wave')

offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)

amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0)

phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)

freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1)
```

---

Sliders Example Walk-through (cont.)

* set up some some callbacks

```
def update_title(attrname, old, new):
    plot.title = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b

    source.data = dict(x=x, y=y)

for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)
```

---

Sliders Example Walk-through (cont.)

* set up some layout and add to the document

```

inputs = VBoxForm(children=[text, offset, amplitude, phase, freq])

curdoc().add_root(HBox(children=[inputs, plot], width=800))
```

---

## Server Wisdom 1 - Data updating

* update your ColumnDataSource in one go

<br />
#### GOOD
```python
new_data = {'x': [...], 'y': [....], ....}
source.data = new_data
```

#### BAD
```python
source.data['x'] = [...]
source.data['y'] = [...]
```

Otherwise, the second way generates extra  unnecesary work, and can also cause visual stutter since `x`, `y` values don't update simulataneouly

---

## Server Wisdom 2 - Session cleanup

To control how the Bokeh server cleans up old sessions (and their callbacks), use the options:

```
--unused-session-lifetime

--check-unused-sessions
```
These are especially important to set if you are using periodic callbacks. 

---

## Server Wisdom 3 - Embedding
If you want to embed a bokeh server app in a page on `foo.com` using `autoload_server` you must configure the bokeh server to accept connections from `foo.com` with an option like: 
```
--allow-websocket-origin foo.com
```

---

## Server Wisdom 4 - `figure`/`Figure`

Some API clunkiness will be improved in 0.12, rules to remember for now:

* lower case (`figure`, `hplot`, `vplot`, etc) automatically add objects to the "current document"
* upper case (`Figure`, `HBox`, `VBox`, etc) DO NOT automatically add objects to the "current document"

typically use upper-case versions when building up more complicated nested layouts. 

---

# Datashader

---

Datashader is a graphics pipeline system for creating meaningful representations of large amounts of data. It breaks the creation of images into 3 steps:

1. Projection

Each record is projected into zero or more bins, based on a specified glyph.

2. Aggregation

Reductions are computed for each bin, compressing the potentially large dataset into a much smaller aggregate.

3. Transformation

These aggregates are then further processed to create an image.

---

# Datashader

![DataShader pipeline](images/dspipe.png)

---

# Datashader

Some pre-executed static example notebooks can be viewed online at 

https://anaconda.org/jbednar/notebooks

---
This morning:

https://github.com/bokeh/bokeh-demos/tree/master/presentations/2016-03-pydata-strata

Getting set-up for this afternoon (installing, downloading the exercise notebooks):

https://github.com/bokeh/bokeh-notebooks/tree/master/tutorial
<hr />
Mailing list: http://groups.google.com/a/continuum.io/forum/#!forum/bokeh

Docs: http://bokeh.pydata.org

---

# Thank you
---

## Hacker-slides how-to

- Separate slides using '`---`' on a blank line
- Write github flavored markdown
- Click 'Present' (top right) when you're ready to talk
- There is also a speaker view, with notes - press '`s`'
- Press '`?`' with focus on the presentation for shortcuts
- <em>You can use html when necessary</em>
- Share the 'Present' URL with anyone you like!

Learn more:
- [RevealJS Demo/Manual](http://lab.hakim.se/reveal-js)
- [RevealJS Project/README](https://github.com/hakimel/reveal.js)
- [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown)

Note:
- Anything after `Note:` will only appear here
