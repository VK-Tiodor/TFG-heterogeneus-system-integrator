from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.repository.base import BaseRepository


class SubtaskRepository(BaseRepository):
    MODEL_CLASS = Subtask
