from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation, FtpDataLocation
from heterogeneous_system_integrator.repository.base import BaseRepository


class ApiDataLocationRepository(BaseRepository):
    MODEL_CLASS = ApiDataLocation


class DbDataLocationRepository(BaseRepository):
    MODEL_CLASS = DbDataLocation


class FtpDataLocationRepository(BaseRepository):
    MODEL_CLASS = FtpDataLocation
