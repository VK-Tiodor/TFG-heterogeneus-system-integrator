from heterogeneous_system_integrator.repository.task import TaskRepository
from heterogeneous_system_integrator.service.base import BaseService


class TaskService(BaseService):
    REPOSITORY_CLASS = TaskRepository
    