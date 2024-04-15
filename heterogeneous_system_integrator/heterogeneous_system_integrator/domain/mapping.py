from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base


class Mapping(Base):
    origin_field_name = models.CharField(null=True, blank=True, help_text='Source field name from where to extract the value. Incompatible with "Constant value"')
    constant_value = models.CharField(null=True, blank=True, help_text='Source constant value. Incompatible with "Origin field name"')
    destination_field_name = models.CharField(help_text='Target field name where the value is going to be stored')

    def save(self, *args, **kwargs):
        if self.origin_field_name and self.constant_value:
            raise IntegrityError('"Origin field name" and "Constant value" are mutually exclusive. Only one must be fulfilled.')
        if not self.origin_field_name and not self.constant_value:
            raise IntegrityError('"Origin field name" or "Constant value" must be fulfilled.')
        return super().save(*args, **kwargs)