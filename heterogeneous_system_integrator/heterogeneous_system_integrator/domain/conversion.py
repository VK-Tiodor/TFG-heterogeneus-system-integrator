from django.db import models

from heterogeneous_system_integrator.domain.base import Base, BaseComparator


class Conversion(Base, BaseComparator):
    conversion_value = models.CharField(help_text='The new value that is going to receive the field when the conditions are met')
    