from heterogeneous_system_integrator.repository.connection import ConnectionRepository
from heterogeneous_system_integrator.service.base import BaseService


class ConnectionService(BaseService):
    REPOSITORY_CLASS = ConnectionRepository
