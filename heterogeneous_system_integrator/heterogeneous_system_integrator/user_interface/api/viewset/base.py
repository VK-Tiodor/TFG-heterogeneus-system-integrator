from django.contrib.admin import ModelAdmin
from django.core.exceptions import ObjectDoesNotExist
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

    def get_object(self):
        id_value = self.kwargs['pk']
        try:
            object_ = self.SERVICE_CLASS.get({'id': int(id_value)})
        except (ValueError, ObjectDoesNotExist):
            object_ = self.SERVICE_CLASS.get({'slug': id_value})
        return object_
    
    def perform_create(self, serializer: ModelSerializer):
        return self.SERVICE_CLASS.create_model(**serializer.data)
    
    def perform_update(self, serializer: ModelSerializer):
        model = serializer.instance
        model.__dict__.update(serializer.validated_data)
        return self.SERVICE_CLASS.save_model(model)
    
    def perform_destroy(self, instance):
        return self.SERVICE_CLASS.delete_model(model=instance)


class BaseAdminViewset(_Base, ModelAdmin):
    SERVICE_CLASS: BaseService = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_fields = [
            field.name for field in self.model._meta.fields
            if field is not ManyToManyField
        ]
        self.list_display = model_fields
        self.list_display_links = model_fields

    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> tuple[QuerySet, bool]:
        duplicates = False
        try:
            search_term = int(search_term)
            return self.SERVICE_CLASS.create_query(filters={'pk': search_term}, order_by=['name']), duplicates
        except Exception:
            return self.SERVICE_CLASS.create_query(filters={'name__icontains': search_term}, order_by=['name']), duplicates

    def save_model(self, request: HttpRequest, obj: Base, form: Form, change: bool) -> None:
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

