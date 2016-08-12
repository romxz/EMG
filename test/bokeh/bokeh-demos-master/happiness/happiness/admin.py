from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Employee, Team, Happiness, UserSession


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )


class HappinessAdmin(admin.ModelAdmin):
    list_filter = ('employee', )
    list_display = ('employee', 'date', 'happiness')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Employee)
admin.site.register(Happiness, HappinessAdmin)
admin.site.register(UserSession)
