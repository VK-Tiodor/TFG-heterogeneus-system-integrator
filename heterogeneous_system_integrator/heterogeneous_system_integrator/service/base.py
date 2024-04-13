from django.db.models import QuerySet, Model

from heterogeneous_system_integrator.repository.base import BaseRepository


class BaseService:
    REPOSITORY_CLASS: BaseRepository = None

    @classmethod
    def create_query(cls, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> QuerySet:
        return cls.REPOSITORY_CLASS.create_query(filters, exclude, order_by, distinct)

    @classmethod
    def union(cls, *querysets: QuerySet) -> QuerySet:
        return cls.REPOSITORY_CLASS.union(*querysets)
    
    @classmethod
    def intersection(cls, *querysets: QuerySet) -> QuerySet:
        return cls.REPOSITORY_CLASS.intersection(*querysets)
    
    @classmethod
    def difference(cls, *querysets: QuerySet) -> QuerySet:
        return cls.REPOSITORY_CLASS.difference(*querysets)
    
    @classmethod
    def get(cls, query: QuerySet = None, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> Model:
        return cls.REPOSITORY_CLASS.get(query, filters, exclude, order_by, distinct)
    
    @classmethod
    def get_or_insert(cls, default_properties: dict, **filters) -> Model:
        return cls.REPOSITORY_CLASS.get_or_insert(default_properties, **filters)
    
    @classmethod
    def update_or_insert(cls, default_properties: dict, **filters) -> Model:
        return cls.REPOSITORY_CLASS.update_or_create(defaults=default_properties, **filters)
    
    @classmethod
    def exists(cls, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        return cls.REPOSITORY_CLASS.exists(query, filters, exclude, order_by, distinct)
    
    @classmethod
    def contains(cls, model: Model, query: QuerySet = None, filters :dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        return cls.REPOSITORY_CLASS.contains(model, query, filters, exclude, order_by, distinct)

    @classmethod
    def select(cls, columns: list = None, query: QuerySet = None, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> list:
        return cls.REPOSITORY_CLASS.select(columns, query, filters, exclude, order_by, distinct)
    
    @classmethod
    def insert(cls, model: Model, models: list[Model], **properties) -> Model:
        return cls.REPOSITORY_CLASS.insert(model, models, **properties)
    
    @classmethod
    def update(cls, model: Model = None, models_and_columns: tuple[list[Model], list[str]] = None, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None, new_values: dict = None) -> int:
        return cls.REPOSITORY_CLASS.update(model, models_and_columns, query, filters, exclude, order_by, distinct, new_values)
    
    @classmethod
    def delete(cls, model: Model = None, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> int:
        return cls.REPOSITORY_CLASS.delete(model, query, filters, exclude, order_by, distinct)
