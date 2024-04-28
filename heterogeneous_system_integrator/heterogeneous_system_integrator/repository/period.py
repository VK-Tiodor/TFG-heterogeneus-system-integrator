from heterogeneous_system_integrator.domain.period import Period
from heterogeneous_system_integrator.repository.base import BaseRepository


class PeriodRepository(BaseRepository):
    MODEL_CLASS = Period
