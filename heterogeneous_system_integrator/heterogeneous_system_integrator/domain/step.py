from django.db import models
from django.db import IntegrityError

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.conversion import Conversion
from heterogeneous_system_integrator.domain.data_location import BaseDataLocation
from heterogeneous_system_integrator.domain.filter import Filter
from heterogeneous_system_integrator.domain.mapping import Mapping


class TransferStep(Base):
    data_location = models.ForeignKey(BaseDataLocation, on_delete=models.PROTECT, related_name='transfer_steps', help_text='Data location where the transfering data process is going to take place')
    filters = models.ManyToManyField(Filter, related_name='transfer_steps', null=True, blank=True, help_text='Filter to select the data that is going to be transfered')

class TransformStep(Base):
    mappings = models.ManyToManyField(Mapping, related_name='transform_steps', help_text='Mappings to choose which data fields are going to be uploaded and from which origin')
    discard_leftover_fields = models.BooleanField(default=True, help_text='Behavior with the data fields that have not been mapped.')
    conversions = models.ManyToManyField(Conversion, related_name='transform_steps', null=True, blank=True, help_text='Conversions to modify the field values that are going to be uploaded')
    conversions_after_mappings = models.BooleanField(null=True, blank=True, help_text='Conversions change values over the specified field names. This process can be done on the original fields or the mapped fields.')
    