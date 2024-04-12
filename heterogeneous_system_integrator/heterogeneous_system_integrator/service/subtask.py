from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository
    