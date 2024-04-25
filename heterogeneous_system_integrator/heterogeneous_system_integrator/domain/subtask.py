from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep


class Subtask(Base):
    download_steps = models.ManyToManyField(TransferStep, related_name='subtasks_download', help_text='Steps that download data')
    merge_field_name = models.CharField(null=True, blank=True, help_text='Field name by which to merge the data. Must be a unique identifier for the objects. Leave blank if there is only one download step.')
    transform_step = models.ForeignKey(TransformStep, on_delete=models.SET_NULL, related_name='subtasks',  null=True, blank=True, help_text='Step that transforms data to the configured format')
    upload_step = models.ForeignKey(TransferStep, on_delete=models.PROTECT, related_name='subtasks_upload', help_text='Step that uploads data')

    def save(self, *args, **kwargs):
        len_download_steps = self.download_steps.count()
        if len_download_steps < 1:
            raise IntegrityError('Download steps must be fulfilled with at least one step.')
        elif len_download_steps > 1 and not self.merge_field_name:
            raise IntegrityError('Merge field name must be fulfilled with a unique identifier when there is more than one download step.')
        return super().save(*args, **kwargs)