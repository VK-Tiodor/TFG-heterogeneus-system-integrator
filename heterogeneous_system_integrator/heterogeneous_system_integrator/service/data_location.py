from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation, FtpDataLocation
from heterogeneous_system_integrator.repository.data_location import ApiDataLocationRepository, DbDataLocationRepository, FtpDataLocationRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.connection import ApiConnectionService, DbConnectionService, FtpConnectionService
from heterogeneous_system_integrator.service.path import ApiPathService, DbPathService, FtpPathService


class ApiDataLocationService(BaseService):
    MODEL_CLASS = ApiDataLocationRepository

    @classmethod
    def download_data(cls, data_location: ApiDataLocation) -> list[dict]:
        url, headers = cls._prepare_data_transfer(data_location)
        data = ApiConnectionService.download_data(url, headers)
        data = ApiPathService.get_clean_data(data, data_location.path)
        return data
    
    @classmethod
    def upload_data(cls, data_location: ApiDataLocation, data: list[dict]) -> list[str]:
        url, headers = cls._prepare_data_transfer(data_location)
        return ApiConnectionService.upload_data(url, headers, data)

    @classmethod
    def _prepare_data_transfer(cls, data_location: ApiDataLocation) -> tuple[dict, dict, str]:
        connection = data_location.connection
        path = data_location.path
        url = ApiPathService.build_full_url(connection, path)
        headers = ApiConnectionService.build_headers(connection)
        return url, headers


#TODO
class DbDataLocationService(BaseService):
    MODEL_CLASS = DbDataLocationRepository

    @classmethod
    def download_data(cls, data_location: DbDataLocation) -> list[dict]:
        pass
    
    @classmethod
    def upload_data(cls, data_location: DbDataLocation, data: list[dict]) -> None:
        pass


#TODO
class FtpDataLocationService(BaseService):
    MODEL_CLASS = FtpDataLocationRepository

    @classmethod
    def download_data(cls, data_location: FtpDataLocation) -> list[dict]:
        pass
    
    @classmethod
    def upload_data(cls, data_location: FtpDataLocation, data: list[dict]) -> None:
        pass
