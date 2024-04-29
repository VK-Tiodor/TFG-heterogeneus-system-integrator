from django.db import models
from django_celery_beat.models import CrontabSchedule

from heterogeneous_system_integrator.domain.base import Base


class Period(Base):
    minute = models.CharField(default='*', help_text='Possible values from 0 to 59. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    hour = models.CharField(default='*', help_text='Possible values from 0 to 23. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    day_of_week = models.CharField(default='*', help_text='Possible values from 1 to 7. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    day_of_month = models.CharField(default='*', help_text='Possible values from 1 to 31. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    month_of_year = models.CharField(default='*', help_text='Possible values from 1 to 12. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    celery_crontab = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True, editable=False)
