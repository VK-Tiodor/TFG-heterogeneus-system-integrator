from heterogeneous_system_integrator.repository.task_result import TaskResultRepository
from heterogeneous_system_integrator.service.base import BaseService


class TaskResultService(BaseService):
    REPOSITORY_CLASS = TaskResultRepository
