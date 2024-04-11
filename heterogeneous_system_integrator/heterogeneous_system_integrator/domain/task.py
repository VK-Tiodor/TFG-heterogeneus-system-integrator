from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.subtask import Subtask


class Task(Base):
    subtasks = models.ManyToManyField(Subtask, related_name='tasks')
    execute_at = models.DateTimeField(null=True, blank=True)
    execute_every_period = models.CharField(
        null=True,
        blank=True, 
        help_text="Please use the following format: Minute[0-59] Hour[0-23] Day[1-31] Month[1-12] Week[0-6](0=Sunday). Syntax guide: Use a space to separate each field, use a comma to separate multiple values, use a hyphen to designate a range of values and use an asterisk as a wildcard to include all possible values. Example: 30 12 * * 0,6 (all saturday and sunday at 12:30)"
    )
    stop_at = models.DateTimeField(null=True, blank=True, help_text='From that point on the task is not going to be executed anymore.')

    def save(self, *args, **kwargs):
        if self.execute_at and self.execute_every_period:
            raise IntegrityError('ERROR: To schedule a task only execute_at or execute_every_period have to be fulfilled, not both.')
        if self.stop_at and not self.execute_every_period:
            raise IntegrityError('ERROR: Scheduling a stop_at date for a task only is possible if execute_every_period is fulfilled too.')
        if self.execute_at or self.execute_every_period:
            # TODO Create periodic task
            pass
        return super().save(*args, **kwargs)