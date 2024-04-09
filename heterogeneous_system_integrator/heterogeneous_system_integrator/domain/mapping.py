from django.db import models

from heterogeneous_system_integrator.domain.base import Base


class Mapping(Base):
    origin_field_name = models.CharField()
    destination_field_name = models.CharField()