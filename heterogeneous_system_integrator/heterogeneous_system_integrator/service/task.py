from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask
from heterogeneous_system_integrator.repository.task import AsyncTaskRepository, PlannedTaskRepository, PeriodicTaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.subtask import SubtaskService


class _BaseTaskService(BaseService):
    
    #TODO save results
    @classmethod
    def run(cls, task):
        task_result = f'Task {str(task)} results: \n'
        for subtask in task.subtasks:
            subtask_result = SubtaskService.run(subtask)
            task_result = f'{task_result}\t {subtask_result}\n'
        return task_result


class AsyncTaskService(_BaseTaskService):
    REPOSITORY_CLASS = AsyncTaskRepository


class PlannedTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PlannedTaskRepository


class PeriodicTaskService(_BaseTaskService):
    REPOSITORY_CLASS = PeriodicTaskRepository