import numpy as np

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg

from .bokeh_utils import update_bokeh_sessions


class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    manager = models.OneToOneField(User)

    def __str__(self):
        return '%s (%s)' % (self.name, self.manager.first_name)

    def get_team_dates_happiness(self, start_date=None, end_date=None):
        employees = self.employee_set.all()
        h_set = Happiness.objects.filter(employee__in=employees).all()
        average_happinesses = h_set.values('date').annotate(average_happiness=Avg('happiness'))
        dates = average_happinesses.values_list('date', flat=True)
        happinesses = average_happinesses.values_list('average_happiness', flat=True)
        return (np.array(dates), np.array(happinesses))


class Employee(models.Model):
    user = models.OneToOneField(User)
    teams = models.ManyToManyField('happiness.Team')

    def __str__(self):
        return '%s (%s)' % (self.user.first_name, self.teams_list)

    @property
    def teams_list(self):
        return ', '.join([team.name for team in self.teams.all()])

    @property
    def latest_happiness(self):
        return self.happiness_set.latest()

    def get_dates_happiness(self):
        h_set = self.happiness_set.all()
        dates = h_set.values_list('date', flat=True)
        happinesses = h_set.values_list('happiness', flat=True)
        return (np.array(dates), np.array(happinesses))


class Happiness(models.Model):
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    happiness = models.DecimalField(decimal_places=0, max_digits=1)

    class Meta:
        unique_together = (('employee', 'date'),)
        get_latest_by = 'date'
        ordering = ['date']

    def __str__(self):
        return '%s %s %s' % (self.employee.user.first_name, self.happiness, self.date)

    def get_absolute_url(self):
        return reverse('individual', kwargs={'pk': self.employee.user.pk})

    def save(self, *args, **kwargs):
        super(Happiness, self).save(*args, **kwargs)
        # When a new value of Happiness is saved.
        # We update all the data for the bokeh sessions.
        # This is not optimized. Things that could be improved:
        #
        # - Send this off to an external process so that the user gets a quicker response
        # - Only update for users affected by this data (only get affected UserSessions)
        update_bokeh_sessions(UserSession.objects.all())


class UserSession(models.Model):
    user = models.ForeignKey(User)
    bokeh_session_id = models.CharField(max_length=64)
