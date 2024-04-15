from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.domain.subtask import Subtask


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository

    @classmethod
    def run(cls, subtask: Subtask):
        pass
    