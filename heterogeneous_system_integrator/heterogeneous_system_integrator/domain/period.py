from django.db import models, IntegrityError
from django_celery_beat.models import CrontabSchedule

from heterogeneous_system_integrator.domain.base import Base


class Period(Base):
    minute = models.CharField(null=True, blank=True, help_text='Possible values from 0 to 59. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    hour = models.CharField(null=True, blank=True, help_text='Possible values from 0 to 23. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    day_of_week = models.CharField(null=True, blank=True, help_text='Possible values from 1 to 7. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    day_of_month = models.CharField(null=True, blank=True, help_text='Possible values from 1 to 31. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    month_of_year = models.CharField(null=True, blank=True, help_text='Possible values from 1 to 12. Use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values')
    celery_crontab = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not any(self.minute, self.hour, self.day_of_week, self.day_of_month, self.month_of_year):
            raise IntegrityError('At least one field must be fulfilled')
        crontab = CrontabSchedule(minute=self.minute, hour=self.hour, day_of_month=self.day_of_month, month_of_year=self.month_of_year, day_of_week=self.day_of_week)
        crontab.save()
        self.celery_crontab = crontab
        return super().save(*args, **kwargs)