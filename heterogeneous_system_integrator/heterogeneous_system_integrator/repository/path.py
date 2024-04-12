from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath
from heterogeneous_system_integrator.repository.base import BaseRepository


class ApiPathRepository(BaseRepository):
    MODEL_CLASS = ApiPath


class DbPathRepository(BaseRepository):
    MODEL_CLASS = DbPath


class FtpPathRepository(BaseRepository):
    MODEL_CLASS = FtpPath
