from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation, FtpDataLocation
from heterogeneous_system_integrator.repository.data_location import ApiDataLocationRepository, DbDataLocationRepository, FtpDataLocationRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.connection import ApiConnectionService, DbConnectionService, FtpConnectionService
from heterogeneous_system_integrator.service.path import ApiPathService, DbPathService, FtpPathService


class ApiDataLocationService(BaseService):
    MODEL_CLASS = ApiDataLocationRepository

    @classmethod
    def download_data(cls, data_location: ApiDataLocation) -> list[dict]:
        connection = data_location.connection
        path = data_location.path
        headers, payload = ApiConnectionService.prepare_message(connection)
        url = ApiPathService.build_full_url(connection, path)
        data = ApiConnectionService.download_data(url, headers, payload)
        data = ApiPathService.get_clean_data(data, path)
        return data


class DbDataLocationService(BaseService):
    MODEL_CLASS = DbDataLocationRepository

    #TODO
    @classmethod
    def download_data(cls, data_location: DbDataLocation) -> list[dict]:
        connection = data_location.connection
        path = data_location.path
        headers, payload = DbConnectionService.prepare_message(connection)
        url = DbPathService.build_full_url(connection, path)
        data = DbConnectionService.download_data(url, headers, payload)
        data = DbPathService.get_clean_data(data, path)
        return data


class FtpDataLocationService(BaseService):
    MODEL_CLASS = FtpDataLocationRepository

    #TODO
    @classmethod
    def download_data(cls, data_location: ApiDataLocation) -> list[dict]:
        connection = data_location.connection
        path = data_location.path
        headers, payload = FtpConnectionService.prepare_message(connection)
        url = FtpPathService.build_full_url(connection, path)
        data = FtpConnectionService.download_data(url, headers, payload)
        data = FtpPathService.get_clean_data(data, path)
        return data
