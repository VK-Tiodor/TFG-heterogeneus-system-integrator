from django_celery_beat.models import CrontabSchedule 
from django.db import models

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.subtask import Subtask


class Task(Base):
    subtasks = models.ManyToManyField(Subtask, related_name='tasks')
    schedule = models.ForeignKey(CrontabSchedule, on_delete=models.SET_NULL, null=True)
    stop_at = models.DateTimeField(null=True, help_text='(Optional) From that point on the task is not going to be executed anymore.')