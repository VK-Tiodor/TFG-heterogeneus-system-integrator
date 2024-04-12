from heterogeneous_system_integrator.repository.conversion import ConversionRepository
from heterogeneous_system_integrator.service.base import BaseService


class ConversionService(BaseService):
    REPOSITORY_CLASS = ConversionRepository
