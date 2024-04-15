from django.db import models

from heterogeneous_system_integrator.domain.base import Base, BaseComparator


FILTER_TYPE = {
    (FILTER_TYPE_KEEP := 'keep'): 'Keep',
    (FILTER_TYPE_DISCARD := 'discard'): 'Discard'
}

class Filter(Base, BaseComparator):
    type = models.CharField(choices=FILTER_TYPE.items(), help_text='Filter behaviour with data when conditions are met')