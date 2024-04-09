from django.db import models

from heterogeneous_system_integrator.domain.base import Base


OPERATOR_TYPES = {
    (OPERATOR_TYPE_EQ := '=='): 'Equal',
    (OPERATOR_TYPE_GT := '>'): 'Greater than',
    (OPERATOR_TYPE_GTE := '>='): 'Greater than or equal to',
    (OPERATOR_TYPE_IN := 'in'): 'In',
    (OPERATOR_TYPE_LT := '<'): 'Less than',
    (OPERATOR_TYPE_LTE := '<='): 'Less than or equal to',
    (OPERATOR_TYPE_NEQ := '!='): 'Not equal',
    (OPERATOR_TYPE_NIN := 'nin'): 'Not in',
}


class Filter(Base):
    field_name = models.CharField(help_text='The field name which value is subject of comparison')
    comparison_operator = models.CharField(choices=list(OPERATOR_TYPES.items()))
    comparison_value = models.CharField(help_text='The value that is going to be compared with.')
