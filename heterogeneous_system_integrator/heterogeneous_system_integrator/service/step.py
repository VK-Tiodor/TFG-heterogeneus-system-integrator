from heterogeneous_system_integrator.repository.step import TransferStepRepository, TransformStepRepository
from heterogeneous_system_integrator.service.base import BaseService


class TransferStepService(BaseService):
    REPOSITORY_CLASS = TransferStepRepository


class TransformStepService(BaseService):
    REPOSITORY_CLASS = TransformStepRepository
