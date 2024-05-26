from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.db.models import ManyToManyField
from django.db.models.query import QuerySet
from django.forms import Form, BaseFormSet
from django.http.request import HttpRequest
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.domain.base import Base


class _Base:
    SERVICE_CLASS: BaseService = None

    def get_queryset(self, request: HttpRequest = None) -> QuerySet:
        return self.SERVICE_CLASS.create_query(order_by=['name'])


class BaseViewset(_Base, ModelViewSet):
    lookup_field = 'slug'

    # TODO -> Revisar acciones, que hay que corregir

    def get_object(self):
        return self.SERVICE_CLASS.get(filters={self.lookup_field: self.kwargs[self.lookup_field]})
    
    def perform_create(self, serializer: ModelSerializer):
        return self.SERVICE_CLASS.create_model(properties=serializer.data)
    
    def perform_update(self, serializer: ModelSerializer):
        return self.SERVICE_CLASS.update(filters={self.lookup_field: serializer.data[self.lookup_field]}, new_values=serializer.data)
    
    def perform_destroy(self, instance):
        return self.SERVICE_CLASS.delete(model=instance)


class BaseAdminViewset(_Base, ModelAdmin):
    SERVICE_CLASS: BaseService = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = [
            field.name for field in self.model._meta.fields
            if field is not ManyToManyField
        ]

    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> tuple[QuerySet, bool]:
        duplicates = False
        try:
            search_term = int(search_term)
            return self.SERVICE_CLASS.create_query(filters={'pk': search_term}, order_by=['name']), duplicates
        except Exception:
            return self.SERVICE_CLASS.create_query(filters={'name__icontains': search_term}, order_by=['name']), duplicates

    def save_model(self, request: HttpRequest, obj: Base, form: Form, change: bool) -> None:
        if change:
            return self.SERVICE_CLASS.save_model(obj)

        relations = {field_name: value for field_name, value in form.cleaned_data.items() if isinstance(value, QuerySet)}
        if not relations:
            return self.SERVICE_CLASS.save_model(obj)
        else:
            return self.SERVICE_CLASS.save_model_with_relations(obj, relations)

    def save_related(self, request: HttpRequest, form: Form, formsets: BaseFormSet, change: bool) -> None:
        pass

    def delete_model(self, request: HttpRequest, obj: Base) -> None:
        self.SERVICE_CLASS.delete_model(model=obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        self.SERVICE_CLASS.delete_query(query=queryset)

