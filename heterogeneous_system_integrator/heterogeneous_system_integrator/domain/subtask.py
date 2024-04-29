from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep


class Subtask(Base):
    download_steps = models.ManyToManyField(TransferStep, related_name='subtasks_download', help_text='Steps that download data')
    merge_field_name = models.CharField(null=True, blank=True, help_text='Field name by which to merge the data. Must be a unique identifier for the objects. Leave blank if there is only one download step.')
    transform_step = models.ForeignKey(TransformStep, on_delete=models.SET_NULL, related_name='subtasks',  null=True, blank=True, help_text='Step that transforms data to the configured format')
    upload_step = models.ForeignKey(TransferStep, on_delete=models.PROTECT, related_name='subtasks_upload', help_text='Step that uploads data')
