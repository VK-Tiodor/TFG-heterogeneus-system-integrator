from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep
from heterogeneous_system_integrator.repository.base import BaseRepository


class TransferStepRepository(BaseRepository):
    MODEL_CLASS = TransferStep


class TransformStepRepository(BaseRepository):
    MODEL_CLASS = TransformStep
