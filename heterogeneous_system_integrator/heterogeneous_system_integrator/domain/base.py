from datetime import datetime

from django.db import models
from django.utils.text import slugify


class Base(models.Model):

    name = models.CharField()
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            timestamp = datetime.strftime(datetime.now(), '%d%m%Y%H%M%S')
            self.slug = slugify(f'{self.name}-{timestamp}')
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        