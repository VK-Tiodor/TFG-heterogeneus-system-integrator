from django.db.models import QuerySet
from django.utils.text import slugify

from heterogeneous_system_integrator.domain.base import Base

class BaseRepository:
    MODEL_CLASS: Base = None
    
    @classmethod
    def create_query(cls, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> QuerySet:
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
    def union(cls, querysets: list[QuerySet]) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        
        return querysets[0].union(*querysets[1:])
    
    @classmethod
    def intersection(cls, querysets: list[QuerySet]) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        
        return querysets[0].intersection(*querysets[1:])
    
    @classmethod
    def difference(cls, querysets: list[QuerySet]) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        
        return querysets[0].difference(*querysets[1:])
    
    @classmethod
    def get(cls, filters: dict = None) -> Base:
        return cls.MODEL_CLASS.objects.get(**filters)

    @classmethod
    def get_or_insert(cls, default_properties: dict, filters: dict) -> Base:
        return cls.MODEL_CLASS.objects.get_or_create(defaults=default_properties, **filters)[0]
    
    @classmethod
    def update_or_insert(cls, default_properties: dict, filters: dict) -> Base:
        return cls.MODEL_CLASS.objects.update_or_create(defaults=default_properties, **filters)[0]
    
    @classmethod
    def select(cls, columns: list, query: QuerySet = None) -> list:
        if not query.exists():
            return []
        
        query = query.values_list(*columns, flat=(len(columns) == 1))
        return list(query)

    @classmethod
    def _pre_save_model_operations(cls, model: Base):
        if not model.slug:
            model.slug = slugify(model.name)

    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[Base], fields: list[str] = None):
        for model in models:
            if not model.slug:
                model.slug = slugify(model.name)
        
        if fields:
            fields += [model.slug.name]
    
    @classmethod
    def _post_save_model_operations(cls, model: Base) -> None:
        pass

    @classmethod
    def _post_save_multiple_models_operations(cls, query: QuerySet) -> None:
        pass

    @classmethod
    def _pre_delete_model_operations(cls, model: Base) -> None:
        pass

    @classmethod
    def _pre_delete_query_operations(cls, query: QuerySet) -> None:
        pass

    @classmethod
    def _post_delete_model_operations(cls, model: Base) -> None:
        pass

    @classmethod
    def _post_delete_query_operations(cls, query: QuerySet) -> None:
        pass

    @classmethod
    def save_model(cls, model: Base) -> Base:
        cls._pre_save_model_operations(model)
        model.save()
        cls._post_save_model_operations(model)
        return model

    @classmethod
    def save_model_with_relations(cls, model: Base, relations: dict) -> Base:
        cls._pre_save_model_operations(model)
        
        if not model.pk:
            model.save()
        
        for field_name, queryset in relations.items():
            field = getattr(model, field_name)
            field.set(objs=list(queryset), clear=True)
        
        model.save()
        cls._post_save_model_operations(model)
        return model

    @classmethod
    def insert_multiple_models(cls, models: list[Base]) -> list[Base]:
        cls._pre_save_multiple_models_operations(models)
        models = cls.MODEL_CLASS.objects.bulk_create(models)
        cls._post_save_multiple_models_operations(models)
        return models
        
    @classmethod
    def update_multiple_models(cls, models: list[Base], field_names: list[str]) -> int:
        cls._pre_save_multiple_models_operations(models, field_names)
        updated_count = cls.MODEL_CLASS.objects.bulk_update(models, field_names)
        cls._post_save_multiple_models_operations(models, field_names)
        return updated_count
    
    @classmethod
    def delete_model(cls, model: Base) -> None:
        cls._pre_delete_model_operations(model)
        model.delete()
        cls._post_delete_model_operations(model)
    
    @classmethod
    def delete_query(cls, query: QuerySet = None) -> int:
        cls._pre_delete_query_operations(query)
        deleted_count = query.delete()[0]
        cls._post_delete_query_operations(query)
        return deleted_count
