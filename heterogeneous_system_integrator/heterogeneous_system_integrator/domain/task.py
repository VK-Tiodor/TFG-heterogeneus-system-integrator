from django.db import models
from django_celery_beat.models import PeriodicTask

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.domain.period import Period


class AsyncTask(Base):
    subtasks = models.ManyToManyField(Subtask, related_name='tasks', help_text='Subtasks that are going to be executed')
    

class PlannedTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='planned_tasks', on_delete=models.CASCADE)
    execute_at = models.DateTimeField(help_text='Date and time when the task is going to be executed')
    celery_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, editable=False)


class PeriodicTask(Base):
    async_task = models.ForeignKey(AsyncTask, related_name='periodic_tasks', on_delete=models.CASCADE)
    period = models.ForeignKey(Period, related_name='periodic_tasks', on_delete=models.PROTECT, help_text='Time pattern used for task execution')
    stop_at = models.DateTimeField(null=True, blank=True, help_text='From that point on the task is not going to be executed anymore and is goint to be deleted')
    celery_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True, editable=False)
