from django.db.models import QuerySet

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.repository.base import BaseRepository


class BaseService:
    REPOSITORY_CLASS: BaseRepository = None

    @classmethod
    def create_query(cls, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> QuerySet:
        return cls.REPOSITORY_CLASS.create_query(filters, exclude, order_by, distinct)

    @classmethod
    def union(cls, querysets: list[QuerySet]) -> QuerySet:
        return cls.REPOSITORY_CLASS.union(*querysets)
    
    @classmethod
    def intersection(cls, querysets: list[QuerySet]) -> QuerySet:
        return cls.REPOSITORY_CLASS.intersection(*querysets)
    
    @classmethod
    def difference(cls, querysets: list[QuerySet]) -> QuerySet:
        return cls.REPOSITORY_CLASS.difference(*querysets)
    
    @classmethod
    def get(cls, filters: dict = None) -> Base:
        return cls.REPOSITORY_CLASS.get(filters)
    
    @classmethod
    def get_or_insert(cls, default_properties: dict, filters: dict) -> Base:
        return cls.REPOSITORY_CLASS.get_or_insert(default_properties, filters)
    
    @classmethod
    def update_or_insert(cls, default_properties: dict, filters: dict) -> Base:
        return cls.REPOSITORY_CLASS.update_or_insert(default_properties, filters)

    @classmethod
    def select(cls, columns: list = None, query: QuerySet = None) -> list:
        return cls.REPOSITORY_CLASS.select(columns, query)
    
    @classmethod
    def save_model(cls, model: Base) -> Base:
        return cls.REPOSITORY_CLASS.save_model(model)

    @classmethod
    def create_model(cls, **field_data) -> Base:
        return cls.REPOSITORY_CLASS.create_model(**field_data)

    @classmethod
    def save_model_with_relations(cls, model: Base, relations: dict):
        return cls.REPOSITORY_CLASS.save_model_with_relations(model, relations)

    @classmethod
    def insert_multiple_models(cls, models: list[Base]) -> list[Base]:
        return cls.REPOSITORY_CLASS.insert_multiple_models(models)
        
    @classmethod
    def update_multiple_models(cls, models: list[Base], columns: list[str]) -> int:
        return cls.REPOSITORY_CLASS.update_multiple_models(models, columns)
    
    @classmethod
    def delete_model(cls, model: Base) -> None:
        return cls.REPOSITORY_CLASS.delete_model(model)
    
    @classmethod
    def delete_query(cls, query: QuerySet = None) -> int:
        return cls.REPOSITORY_CLASS.delete_query(query)
