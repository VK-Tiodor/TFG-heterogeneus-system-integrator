import json

from django import forms
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django_celery_results.models import TaskResult

from heterogeneous_system_integrator.service.task_result import TaskResultService
from heterogeneous_system_integrator.user_interface.api.serializer.task_result import TaskResultSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseTaskResultViewset:
    SERVICE_CLASS = TaskResultService

    def get_queryset(self, request: HttpRequest = None) -> QuerySet:
        return self.SERVICE_CLASS.create_query(order_by=['date_done'])


class TaskResultViewset(_BaseTaskResultViewset, BaseViewset):
    serializer_class = TaskResultSerializer


class TaskResultAdminViewset(_BaseTaskResultViewset, BaseAdminViewset):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display.pop(self.list_display.index('result'))
        self.readonly_fields = self.list_display + ['result']

    def get_search_results(self, request: HttpRequest, queryset: QuerySet, search_term: str) -> tuple[QuerySet, bool]:
        duplicates = False
        if not search_term:
            return queryset, duplicates

        try:
            search_term = int(search_term)
            return self.SERVICE_CLASS.create_query(filters={'pk': search_term}, order_by=['name']), duplicates
        except Exception:
            return self.SERVICE_CLASS.create_query(filters={'task_name__icontains': search_term}, order_by=['date_done']), duplicates
