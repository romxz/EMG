from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral9

from .utils import make_plot, make_legend


def update_individuals_data(user, session):
    employees = user.team.employee_set.all()
    for employee in employees:
        dates, happiness = employee.get_dates_happiness()
        source = session.document.select_one({'name': str(employee.pk)})
        source.data = dict(x=dates, y=happiness)


def make_individuals_plot(user):
    plot = make_plot()
    legends = []
    employees = user.team.employee_set.all()
    for i, employee in enumerate(employees):
        dates, happiness = employee.get_dates_happiness()
        source = ColumnDataSource(
            data=dict(x=dates, y=happiness),
            name=str(employee.pk)
        )
        line = plot.line(
            x='x', y='y', source=source,
            line_width=2, line_cap='round', line_color=Spectral9[i]
        )
        legends.append((employee.user.first_name, [line]))
    plot.add_layout(make_legend(legends=legends))
    return plot
