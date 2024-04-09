from django.db import models

from heterogeneous_system_integrator.domain.filter import Filter


class Conversion(Filter):
    conversion_value = models.CharField(help_text='The new value that is going to receive the field if the comparison is true.')
    