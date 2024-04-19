from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, PeriodicTask

from heterogeneous_system_integrator.settings import CELERY_PLANNED_TASK_NAME, CELERY_PERIODIC_TASK_NAME
from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.subtask import Subtask


class AsyncTask(Base):
    subtasks = models.ManyToManyField(Subtask, related_name='tasks', help_text='Subtasks that are going to be executed')
    

class PlannedTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='planned_tasks', on_delete=models.CASCADE)
    execute_at = models.DateTimeField(help_text='Date and time when the task is going to be executed')

    def save(self, *args, **kwargs):
        if (datetime(self.execute_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Execute at" must be fulfilled with a date in the future')
        cs = ClockedSchedule(clocked_time=self.execute_at).save()
        PeriodicTask(name=self.name, task=CELERY_PLANNED_TASK_NAME, clocked=cs, kwargs={"task": self}).save()
        return super().save(*args, **kwargs)


class PeriodicTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='periodic_tasks', on_delete=models.CASCADE)
    period = models.CharField(
        help_text="Please use the following format: Minute[0-59] Hour[0-23] Day[1-31] Month[1-12] Week[0-6](0=Sunday).\
            Syntax guide: Use a space to separate each field, use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values.\
            Example: 30 12 * * 0,6 (all saturday and sunday at 12:30)"
    )
    stop_at = models.DateTimeField(null=True, blank=True, help_text='From that point on the task is not going to be executed anymore and is goint to be deleted')

    def save(self, *args, **kwargs):
        if self.stop_at and (datetime(self.stop_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Stop at" must be fulfilled with a date in the future')    
        minute, hour, day_of_month, month_of_year, day_of_week = self.period.split()
        cs = CrontabSchedule(minute=minute, hour=hour, day_of_month=day_of_month, month_of_year=month_of_year, day_of_week=day_of_week).save()
        PeriodicTask(name=self.name, task=CELERY_PERIODIC_TASK_NAME, crontab=cs, kwargs={"task": self}, expires=self.stop_at).save()
        return super().save(*args, **kwargs)
