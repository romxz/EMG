from bokeh.plotting import Figure
from bokeh.models import Range1d, Legend, FixedTicker


def make_plot():
    plot = Figure(
        plot_height=400,
        plot_width=800,
        responsive=True,
        tools="xpan,xwheel_zoom,xbox_zoom,reset",
        x_axis_type='datetime',
        min_border_top=10,
        min_border_right=0,
        min_border_bottom=0,
        min_border_left=30,
        outline_line_color=None,
    )
    plot.x_range.follow = "end"
    plot.x_range.follow_interval = 120 * 24 * 60 * 60 * 1000
    plot.x_range.range_padding = 0
    plot.y_range = Range1d(0, 12)
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.yaxis.bounds = (0, 9)
    plot.yaxis.minor_tick_line_color = None
    plot.yaxis.ticker = FixedTicker(ticks=[0, 3, 6, 9])
    return plot


def make_legend(legends):
    return Legend(
        legends=legends,
        location='top_right',
        border_line_color=None,
        background_fill_alpha=0.7
    )
