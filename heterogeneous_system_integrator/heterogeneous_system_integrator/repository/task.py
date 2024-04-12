from heterogeneous_system_integrator.domain.task import Task
from heterogeneous_system_integrator.repository.base import BaseRepository


class TaskRepository(BaseRepository):
    MODEL_CLASS = Task
