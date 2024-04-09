from django.db import models

class BaseRepository:
    
    MODEL_CLASS: models.Model = None

    @classmethod
    def retrieve(cls, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> models.QuerySet:
        qs = cls.MODEL_CLASS.objects.all()
        if filters:
            qs = qs.filter(**filters)
        if exclude:
            qs = qs.exclude(**exclude)
        if order_by:
            qs = qs.order_by(*order_by)
        if distinct:
            qs = qs.distinct(*distinct)
        return qs
    
    @classmethod
    def union(cls, *querysets: models.QuerySet) -> models.QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].union(querysets[1:])
    
    @classmethod
    def intersection(cls, *querysets: models.QuerySet) -> models.QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].intersection(querysets[1:])
    
    @classmethod
    def difference(cls, *querysets: models.QuerySet) -> models.QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].difference(querysets[1:])
    
    @classmethod
    def get(cls, **filters) -> models.Model:
        return cls.MODEL_CLASS.objects.get(**filters)
    
    @classmethod
    def create(cls, **properties) -> None:
        return cls.MODEL_CLASS.objects.create(**properties)

    @classmethod
    def get_or_create(cls, defaults: dict, **filters_properties, ) -> models.Model:
        return cls.MODEL_CLASS.objects.get_or_create(defaults=defaults, **filters_properties)[0]