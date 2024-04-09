from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.connection import Connection
from heterogeneous_system_integrator.domain.conversion import Conversion
from heterogeneous_system_integrator.domain.filter import Filter
from heterogeneous_system_integrator.domain.mapping import Mapping


class TransferStep(Base):
    connection = models.ForeignKey(Connection, on_delete=models.PROTECT, related_name='transfer_steps')
    filter = models.ForeignKey(Filter, on_delete=models.SET_NULL, null=True, related_name='transfer_steps')

class TransformStep(Base):
    mappings = models.ManyToManyField(Mapping, related_name='transform_steps')
    conversion = models.ManyToManyField(Conversion, related_name='transform_steps')
