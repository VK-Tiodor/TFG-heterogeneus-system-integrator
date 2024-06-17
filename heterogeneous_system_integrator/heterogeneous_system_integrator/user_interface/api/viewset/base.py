from django.contrib.admin import ModelAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ManyToManyField
from django.db.models.query import QuerySet
from django.forms import Form, BaseFormSet
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_model = self.SERVICE_CLASS.create_model(**serializer.validated_data)
        serializer = self.serializer_class(new_model)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        model = serializer.instance
        model.__dict__.update(serializer.validated_data)
        self.SERVICE_CLASS.save_model(model)
        serializer = self.serializer_class(model)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        self.SERVICE_CLASS.delete_model(model=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

