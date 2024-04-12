from heterogeneous_system_integrator.repository.filter import FilterRepository
from heterogeneous_system_integrator.service.base import BaseService


class FilterService(BaseService):
    REPOSITORY_CLASS = FilterRepository
