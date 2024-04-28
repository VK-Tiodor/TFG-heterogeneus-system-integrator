from heterogeneous_system_integrator.repository.period import PeriodRepository
from heterogeneous_system_integrator.service.base import BaseService


class PeriodService(BaseService):
    REPOSITORY_CLASS = PeriodRepository
