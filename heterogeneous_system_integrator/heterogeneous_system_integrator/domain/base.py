import operator

from django.db import models


OPERATOR_TYPES = {
    (OPERATOR_TYPE_EQ := '=='): 'Equal',
    (OPERATOR_TYPE_GT := '>'): 'Greater than',
    (OPERATOR_TYPE_GTE := '>='): 'Greater than or equal to',
    (OPERATOR_TYPE_IN := 'in'): 'In',
    (OPERATOR_TYPE_LT := '<'): 'Less than',
    (OPERATOR_TYPE_LTE := '<='): 'Less than or equal to',
    (OPERATOR_TYPE_NOT_EQ := '!='): 'Not equal',
    (OPERATOR_TYPE_NOT_IN := 'nin'): 'Not in',
}


OPERATIONS = {
    OPERATOR_TYPE_EQ: operator.eq,
    OPERATOR_TYPE_GT: operator.gt,
    OPERATOR_TYPE_GTE: operator.ge,
    OPERATOR_TYPE_IN: operator.contains,
    OPERATOR_TYPE_LT: operator.lt,
    OPERATOR_TYPE_LTE: operator.le,
    OPERATOR_TYPE_NOT_EQ: (lambda x, y: operator.not_(operator.eq(x, y))),
    OPERATOR_TYPE_NOT_IN: (lambda x, y: operator.not_(operator.contains(x, y))),
}


class Base(models.Model):

    name = models.CharField(unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        

class BaseComparator(models.Model):
    field_name = models.CharField(help_text='The field name which value is subject of comparison')
    comparison_operator = models.CharField(choices=list(OPERATOR_TYPES.items()))
    comparison_value = models.CharField(help_text='The value that is going to be compared with')

    class Meta:
        abstract = True


class BaseConnection(models.Model):
    hostname = models.CharField(help_text='www.host_site.com or 192.168.0.1')
    port = models.IntegerField(null=True, blank=True, help_text='5432')
    username = models.CharField(null=True, blank=True)
    password = models.CharField(null=True, blank=True)

    class Meta:
        abstract = True
