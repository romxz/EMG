from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral4

from .utils import make_plot


def update_teams_data(user, session):
    dates, happiness = user.team.get_team_dates_happiness()
    source = session.document.select_one({'type': ColumnDataSource})
    source.data = dict(x=dates, y=happiness)


def make_teams_plot(user):
    plot = make_plot()
    plot.plot_height = 200
    plot.y_range.end = 9
    dates, happiness = user.team.get_team_dates_happiness()
    plot.line(
        x=dates, y=happiness,
        line_width=2, line_color=Spectral4[3], line_cap='round',
    )
    return plot
