from heterogeneous_system_integrator.repository.mapping import MappingRepository
from heterogeneous_system_integrator.service.base import BaseService


class MappingService(BaseService):
    REPOSITORY_CLASS = MappingRepository
