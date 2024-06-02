from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):
    
    @classmethod
    def run(cls, id, name, slug, created_at, updated_at, subtasks, **kwargs):
        task_result = '%' + (' ' * 35) + f'TASK {name} RESULTS' + (' ' * 35) + '%'
        task_result = '\n' + ('%' * len(task_result)) + f'\n{task_result}\n' + ('%' * len(task_result)) + '\n\n'
        for subtask in SubtaskService.create_query({'pk__in': subtasks}):
            subtask_result = SubtaskService.run(subtask)
            subtask_msg_separator = '|' + (' ' * 35) + f'SUBTASK {str(subtask)} LOGS' + ' ' * 35 + '|'
            subtask_msg_separator = ('-' * len(subtask_msg_separator)) + f'\n{subtask_msg_separator}\n' + ('-' * len(subtask_msg_separator)) + '\n\n'
            task_result = f'{task_result}{subtask_msg_separator}{subtask_result}\n'
        return task_result


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository
