from heterogeneous_system_integrator.celery import app

from heterogeneous_system_integrator.domain.task import CELERY_ASYNC_TASK_NAME, CELERY_PERIODIC_TASK_NAME, CELERY_PLANNED_TASK_NAME
from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):

    @classmethod
    def run(cls, pk):
        task = cls.REPOSITORY_CLASS.get(filters={'pk': pk})
        for subtask in task.subtasks:
            SubtaskService.run(subtask)


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository

    @app.task(bind=True, name=CELERY_ASYNC_TASK_NAME)
    @classmethod
    def run(cls, pk):
        return super().run(pk)

class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository

    @app.task(bind=True, name=CELERY_PLANNED_TASK_NAME)
    @classmethod
    def run(cls, pk):
        return super().run(pk)


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository

    @app.task(bind=True, name=CELERY_PERIODIC_TASK_NAME)
    @classmethod
    def run(cls, pk):
        return super().run(pk)
