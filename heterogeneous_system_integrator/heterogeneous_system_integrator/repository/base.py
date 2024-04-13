from django.db.models import QuerySet, Model


class BaseRepository:
    MODEL_CLASS: Model = None
    
    @classmethod
    def create_query(cls, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> QuerySet:
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
    def union(cls, *querysets: QuerySet) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].union(querysets[1:])
    
    @classmethod
    def intersection(cls, *querysets: QuerySet) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].intersection(querysets[1:])
    
    @classmethod
    def difference(cls, *querysets: QuerySet) -> QuerySet:
        if len(querysets) < 2:
            raise TypeError('Operation needs at least two querysets')
        return querysets[0].difference(querysets[1:])
    
    @classmethod
    def get(cls, query: QuerySet = None, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> Model:
        query = query or cls.create_query(filters, exclude, order_by, distinct)
        return query.get(**filters)

    @classmethod
    def get_or_insert(cls, default_properties: dict, **filters) -> Model:
        return cls.MODEL_CLASS.objects.get_or_create(defaults=default_properties, **filters)[0]
    
    @classmethod
    def update_or_insert(cls, default_properties: dict, **filters) -> Model:
        return cls.MODEL_CLASS.objects.update_or_create(defaults=default_properties, **filters)[0]
    
    @classmethod
    def exists(cls, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        query = query or cls.create_query(filters, exclude, order_by, distinct)
        return query.exists()
    
    @classmethod
    def contains(cls, model: Model, query: QuerySet = None, filters :dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> bool:
        query = query or cls.create_query(filters, exclude, order_by, distinct)
        return query.contains(model)
    
    @classmethod
    def select(cls, columns: list = None, query: QuerySet = None, filters:dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> list:
        query = query or cls.create_query(filters, exclude, order_by, distinct)
        if columns:
            query = query.values_list(*columns, flat=(len(columns) == 1))
        return list(query)

    @classmethod
    def insert(cls, model: Model = None, models: list[Model] = None, **properties) -> None:
        if model:
            model.save()
        elif models:
            cls.MODEL_CLASS.objects.bulk_create(models)
        elif properties:
            cls.MODEL_CLASS.objects.create(**properties)

    @classmethod
    def update(cls, model: Model = None, models_and_columns: tuple[list[Model], list[str]] = None, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None, new_values: dict = None) -> int:
        count = 0
        if model:
            count += 1
            model.save()
        elif models_and_columns:
            count = cls.MODEL_CLASS.objects.bulk_update(models_and_columns[0], models_and_columns[1])
        elif new_values:
            query = query or cls.create_query(filters, exclude, order_by, distinct)
            count = query.update(**new_values)
        return count
    
    @classmethod
    def delete(cls, model: Model = None, query: QuerySet = None, filters: dict = None, exclude: dict = None, order_by: list = None, distinct: list = None) -> int:
        count = 0
        if model:
            count += 1
            model.delete()
        else:
            query = query or cls.create_query(filters, exclude, order_by, distinct)
            count = query.delete()[0]
        return count