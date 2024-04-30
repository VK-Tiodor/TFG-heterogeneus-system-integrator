from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask
from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):
    
    @classmethod
    def run(cls, id, name, slug, created_at, updated_at, subtasks, **kwargs):
        task_result = '\n' + '%' * 32 + ' ' * 4 + f'TASK {name} RESULTS' + ' ' * 4 + '%' * 32 + '\n'
        for subtask in SubtaskService.create_query({'pk__in': subtasks}):
            subtask_result = SubtaskService.run(subtask)
            subtask_msg_separator = '#' * 32 + ' ' * 4 + f'SUBTASK {str(subtask)} RESULTS' + ' ' * 4 + '#' * 32
            task_result = f'{task_result}{subtask_msg_separator}\n\n\n{subtask_result}\n\n\n'
        return task_result


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository