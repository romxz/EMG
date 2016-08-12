from datetime import timedelta

from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .bokeh_utils import get_bokeh_script
from .forms import HappinessForm
from .models import Team, Happiness
from .viz.individual import make_individual_plot
from .viz.individuals import make_individuals_plot
from .viz.team import make_team_plot
from .viz.teams import make_teams_plot


class ContextMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ContextMixin, self).get_context_data(*args, **kwargs)
        users = User.objects.filter(is_superuser=False).order_by('username')
        teams = Team.objects.all().order_by('name')
        context.update(all_users=users, all_teams=teams)
        return context


class HomeView(ContextMixin, TemplateView):
    template_name = 'happiness/home.html'


class IndividualDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_individual.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(IndividualDashboardView, self).get_context_data(*args, **kwargs)
        context.update(
            dashboard='individual'
        )
        if hasattr(self.object, 'employee'):
            plot = make_individual_plot(user=self.object)
            individual_script = get_bokeh_script(user=self.object, plot=plot, suffix='individual')
            latest_date = self.object.employee.latest_happiness.date
            context.update(
                individual_script=individual_script,
                form=HappinessForm(initial={'date': latest_date + timedelta(days=1)}),
            )
        if hasattr(self.object, 'team'):
            plot = make_individuals_plot(user=self.object)
            individuals_script = get_bokeh_script(user=self.object, plot=plot, suffix='individuals')
            context.update(individuals_script=individuals_script)
        return context


class TeamDashboardView(ContextMixin, DetailView):
    template_name = 'happiness/dashboard_team.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, *args, **kwargs):
        context = super(TeamDashboardView, self).get_context_data(*args, **kwargs)
        context.update(dashboard='team')
        if hasattr(self.object, 'employee'):
            plot = make_team_plot(user=self.object)
            team_script = get_bokeh_script(user=self.object, plot=plot, suffix='team')
            context.update(team_script=team_script)
        if hasattr(self.object, 'team'):
            plot = make_teams_plot(user=self.object)
            teams_script = get_bokeh_script(user=self.object, plot=plot, suffix='teams')
            context.update(teams_script=teams_script)
        return context


#################### Happiness Views

class AddHappinessView(CreateView):
    model = Happiness
    fields = ('date', 'happiness')
    template_name = 'happiness/add_happiness.html'

    def dispatch(self, *args, **kwargs):
        self.user_pk = kwargs.get('pk')
        return super(AddHappinessView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = User.objects.get(pk=self.user_pk)
        form.instance.employee = user.employee
        return super(AddHappinessView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AddHappinessView, self).get_context_data(*args, **kwargs)
        context.update(user=User.objects.get(pk=self.user_pk))
        return context
