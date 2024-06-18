from http import HTTPMethod

from django.contrib import messages
from django.contrib.admin import action
from django.http.request import HttpRequest
from django.utils.text import get_text_list
from rest_framework import status
from rest_framework.decorators import action as api_action
from rest_framework.response import Response

from heterogeneous_system_integrator.celery import run_async_task
from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.service.task import AsyncTaskService, PlannedTaskService, PeriodicTaskService
from heterogeneous_system_integrator.user_interface.api.serializer.task import AsyncTaskSerializer, PlannedTaskSerializer, PeriodicTaskSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseAsyncTaskViewset:
    SERVICE_CLASS = AsyncTaskService


# TODO add execution endpoint
class AsyncTaskViewset(_BaseAsyncTaskViewset, BaseViewset):
    serializer_class = AsyncTaskSerializer

    @api_action(detail=True, methods=[HTTPMethod.GET])
    def execute(self, *args, **kwargs):
        try:
            task = self.get_object()
            run_async_task.delay(**AsyncTaskSerializer(task).data)
            response = Response({'executing': {'id': task.id, 'name': task.name}}, status.HTTP_200_OK)
        except Exception as ex:
            response = Response({'executing': None, 'error': str(ex)}, status.HTTP_400_BAD_REQUEST)

        return response


@action(description='Execute tasks')
def execute_tasks(self, request, queryset):
    task_names = []
    for task in queryset:
        run_async_task.delay(**AsyncTaskSerializer(task).data)
        task_names += [str(task)]

    messages.add_message(
        request, messages.INFO, f'Async tasks {get_text_list(task_names, "and")} {"have" if len(task_names) > 1 else "has"} been queued for execution.'
    )


class AsyncTaskAdminViewset(_BaseAsyncTaskViewset, BaseAdminViewset):
    actions = [execute_tasks]

    def response_post_save_change(self, request: HttpRequest, obj: Base):
        if '_execute' in request.POST:
            run_async_task.delay(**AsyncTaskSerializer(obj).data)
            messages.add_message(request, messages.INFO, f'Async task {str(obj)} has been queued for execution.')
        return super().response_post_save_change(request, obj)


class _BasePlannedTaskViewset:
    SERVICE_CLASS = PlannedTaskService


class PlannedTaskViewset(_BasePlannedTaskViewset, BaseViewset):
    serializer_class = PlannedTaskSerializer


class PlannedTaskAdminViewset(_BasePlannedTaskViewset, BaseAdminViewset):
    serializer_class = PlannedTaskSerializer


class _BasePeriodicTaskViewset:
    SERVICE_CLASS = PeriodicTaskService


class PeriodicTaskViewset(_BasePeriodicTaskViewset, BaseViewset):
    serializer_class = PeriodicTaskSerializer


class PeriodicTaskAdminViewset(_BasePeriodicTaskViewset, BaseAdminViewset):
    serializer_class = PeriodicTaskSerializer
