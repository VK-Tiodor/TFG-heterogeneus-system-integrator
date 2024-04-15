from django.db import models
from django.utils.text import slugify


OPERATOR_TYPES = {
    (OPERATOR_TYPE_CONTAINS := 'contains'): 'Contains',
    (OPERATOR_TYPE_EQ := '=='): 'Equal',
    (OPERATOR_TYPE_GT := '>'): 'Greater than',
    (OPERATOR_TYPE_GTE := '>='): 'Greater than or equal to',
    (OPERATOR_TYPE_IN := 'in'): 'In',
    (OPERATOR_TYPE_LT := '<'): 'Less than',
    (OPERATOR_TYPE_LTE := '<='): 'Less than or equal to',
    (OPERATOR_TYPE_NOT_CONTAINS := 'ncontains'): 'Not contains',
    (OPERATOR_TYPE_NOT_EQ := '!='): 'Not equal',
    (OPERATOR_TYPE_NOT_IN := 'nin'): 'Not in',
}


class Base(models.Model):

    name = models.CharField(unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
