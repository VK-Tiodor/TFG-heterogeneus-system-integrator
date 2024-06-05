from celery import states

from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):
    
    @classmethod
    def run(cls, id, name, slug, created_at, updated_at, subtasks, **kwargs) -> dict:
        result = {'task': name, 'status': '', 'duration': 0, 'errors': 0, 'subtasks': []}
        for subtask in SubtaskService.create_query({'pk__in': subtasks}):
            subtask_result = SubtaskService.run(subtask)
            result['subtasks'] += [subtask_result]
            result['errors'] += subtask_result['errors']
            result['duration'] += subtask_result['duration']

        result['status'] = states.SUCCESS if not subtask_result['errors'] else states.FAILURE
        return result


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository
