from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from heterogeneous_system_integrator.settings import CELERY_PLANNED_TASK_NAME, CELERY_PERIODIC_TASK_NAME
from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.domain.period import Period


class AsyncTask(Base):
    subtasks = models.ManyToManyField(Subtask, related_name='tasks', help_text='Subtasks that are going to be executed')
    

class PlannedTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='planned_tasks', on_delete=models.CASCADE)
    execute_at = models.DateTimeField(help_text='Date and time when the task is going to be executed')
    celery_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if (datetime(self.execute_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Execute at" must be fulfilled with a date in the future')
        clock = ClockedSchedule(clocked_time=self.execute_at)
        clock.save()
        properties = dict(name=self.name, task=CELERY_PLANNED_TASK_NAME, clocked=clock, kwargs={"task": self})
        planned_task = PeriodicTask.objects.update_or_create(defaults=properties, name=self.name)[0]
        self.celery_task = planned_task
        return super().save(*args, **kwargs)


class PeriodicTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='periodic_tasks', on_delete=models.CASCADE)
    period = models.ForeignKey(Period, related_name='periodic_tasks', on_delete=models.PROTECT, help_text='Time pattern used for task execution')
    stop_at = models.DateTimeField(null=True, blank=True, help_text='From that point on the task is not going to be executed anymore and is goint to be deleted')
    celery_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.stop_at and (datetime(self.stop_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Stop at" must be fulfilled with a date in the future')
        properties = dict(name=self.name, task=CELERY_PERIODIC_TASK_NAME, crontab=self.period.celery_crontab, kwargs={"task": self}, expires=self.stop_at)
        periodic_task = PeriodicTask.objects.update_or_create(defaults=properties, name=self.name)[0]
        self.celery_task = periodic_task
        return super().save(*args, **kwargs)
