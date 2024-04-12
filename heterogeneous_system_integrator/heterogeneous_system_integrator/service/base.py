from django.db.models import QuerySet, Model

from heterogeneous_system_integrator.repository.base import BaseRepository


class BaseService:
    REPOSITORY_CLASS: BaseRepository = None

    @classmethod
    def create_query(cls, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> QuerySet:
        return cls.REPOSITORY_CLASS.create_query(filters, exclude, order_by, distinct)

    @classmethod
    def select(cls, columns: list = None, query: QuerySet = None, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> list:
        return cls.REPOSITORY_CLASS.select(columns, query, filters, exclude, order_by, distinct)

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
    def create(cls, **properties) -> Model:
        return cls.REPOSITORY_CLASS.create(**properties)

    @classmethod
    def get_or_create(cls, default_properties: dict, **filters) -> Model:
        return cls.REPOSITORY_CLASS.get_or_create(default_properties, **filters)
    
    @classmethod
    def exists(cls, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        return cls.REPOSITORY_CLASS.exists(query, filters, exclude, order_by, distinct)
    
    @classmethod
    def contains(cls, model: Model, query: QuerySet = None, filters :dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        return cls.REPOSITORY_CLASS.contains(model, query, filters, exclude, order_by, distinct)
    
    @classmethod
    def update(cls, new_values: dict, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> int:
        return cls.REPOSITORY_CLASS.update(new_values, query, filters, exclude, order_by, distinct)
    
    @classmethod
    def delete(cls, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> int:
        return cls.REPOSITORY_CLASS.delete(query, filters, exclude, order_by, distinct)