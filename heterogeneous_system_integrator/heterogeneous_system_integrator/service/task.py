from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):

    @classmethod
    def run(cls, task):
        for subtask in task.subtasks:
            SubtaskService.run(subtask)


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository
