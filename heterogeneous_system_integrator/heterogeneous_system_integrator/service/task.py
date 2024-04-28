from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask
from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):
    
    @classmethod
    def run(cls, task):
        task_result = ''
        for subtask in task.subtasks:
            subtask_result = SubtaskService.run(subtask)
            subtask_msg_separator = f"{'#' * 32}{' ' * 4}{str(subtask)}{' ' * 4}{'#' * 32}"
            task_result = f'{task_result}{subtask_msg_separator}\n{subtask_result}\n'
        return task_result


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository