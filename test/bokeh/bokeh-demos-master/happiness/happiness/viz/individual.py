from .utils import make_plot


def make_individual_plot(user):
    plot = make_plot()
    plot.plot_height = 200
    plot.y_range.end = 9
    dates, happiness = user.employee.get_dates_happiness()
    plot.line(
        x=dates, y=happiness,
        line_width=1, line_alpha=0.6, line_color='magenta', line_cap='round',
    )
    return plot
