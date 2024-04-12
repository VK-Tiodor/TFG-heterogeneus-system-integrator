from heterogeneous_system_integrator.domain.connection import Connection
from heterogeneous_system_integrator.repository.base import BaseRepository


class ConnectionRepository(BaseRepository):
    MODEL_CLASS = Connection
