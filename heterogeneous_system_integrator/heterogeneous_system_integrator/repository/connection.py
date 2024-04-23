from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection
from heterogeneous_system_integrator.repository.base import BaseRepository


class ApiConnectionRepository(BaseRepository):
    MODEL_CLASS = ApiConnection


class DbConnectionRepository(BaseRepository):
    MODEL_CLASS = DbConnection


class FtpConnectionRepository(BaseRepository):
    MODEL_CLASS = FtpConnection
