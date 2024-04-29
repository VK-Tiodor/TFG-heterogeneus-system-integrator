from django.db import models

from heterogeneous_system_integrator.domain.base import Base


class Mapping(Base):
    origin_field_name = models.CharField(null=True, blank=True, help_text='Source field name from where to extract the value, in case of inner fields use dots (.) to route. Incompatible with "Constant value"')
    constant_value = models.CharField(null=True, blank=True, help_text='Source constant value. Incompatible with "Origin field name"')
    destination_field_name = models.CharField(help_text='Target field name where the value is going to be stored')
