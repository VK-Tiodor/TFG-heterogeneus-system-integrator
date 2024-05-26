from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation, FtpDataLocation
from heterogeneous_system_integrator.repository.data_location import ApiDataLocationRepository, DbDataLocationRepository, FtpDataLocationRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.connection import ApiConnectionService, DbConnectionService, FtpConnectionService


class ApiDataLocationService(BaseService):
    REPOSITORY_CLASS = ApiDataLocationRepository

    @classmethod
    def _get_clean_data(cls, data: dict, data_location: ApiDataLocation) -> list[dict]:
        for obj_name in data_location.path_to_results_list.split('.'):
            if data.get(obj_name):
                data = data[obj_name]

            else:
                raise TypeError(
                    f'Path to the results list from API Data Location {str(data_location)} config is incorrect. '
                    f'There is no such field as {obj_name} in the request response'
                )

        return data

    @classmethod
    def _prepare_data_transfer(cls, data_location: ApiDataLocation) -> tuple[str, dict]:
        connection = data_location.connection
        url = ApiConnectionService.build_full_url(connection, data_location.endpoint)
        headers = ApiConnectionService.build_headers(connection)
        return url, headers

    @classmethod
    def download_data(cls, data_location: ApiDataLocation) -> list[dict]:
        url, headers = cls._prepare_data_transfer(data_location)
        data = ApiConnectionService.download_data(url, headers)
        data = cls._get_clean_data(data, data_location)
        return data
    
    @classmethod
    def upload_data(cls, data_location: ApiDataLocation, data: list[dict]) -> list[str]:
        url, headers = cls._prepare_data_transfer(data_location)
        return ApiConnectionService.upload_data(url, headers, data)


# TODO
class DbDataLocationService(BaseService):
    REPOSITORY_CLASS = DbDataLocationRepository

    @classmethod
    def download_data(cls, data_location: DbDataLocation) -> list[dict]:
        pass
    
    @classmethod
    def upload_data(cls, data_location: DbDataLocation, data: list[dict]) -> None:
        pass


# TODO
class FtpDataLocationService(BaseService):
    REPOSITORY_CLASS = FtpDataLocationRepository

    @classmethod
    def download_data(cls, data_location: FtpDataLocation) -> list[dict]:
        pass
    
    @classmethod
    def upload_data(cls, data_location: FtpDataLocation, data: list[dict]) -> None:
        pass
