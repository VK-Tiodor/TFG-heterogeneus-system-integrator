from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection
from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath
from heterogeneous_system_integrator.repository.path import ApiPathRepository, DbPathRepository, FtpPathRepository
from heterogeneous_system_integrator.service.base import BaseService


class ApiPathService(BaseService):
    REPOSITORY_CLASS = ApiPathRepository

    @classmethod
    def get_clean_data(cls, data: dict, path: ApiPath) -> dict:
        for obj_name in path.path_to_results_list.split('.'):
            if data.get(obj_name):
                data = data[obj_name]
            else:
                raise TypeError(f'Path to the results list from API Path {str(path)} config is incorrect. There is no such field as {obj_name} in the request response')
        return data

    @classmethod
    def build_full_url(cls, connection: ApiConnection, endpoint: str) -> str:
        url = connection.hostname
        url = url[:-1] if url.endswith('/') else url
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        return f'{url}/{endpoint}'


class DbPathService(BaseService):
    REPOSITORY_CLASS = DbPathRepository


class FtpPathService(BaseService):
    REPOSITORY_CLASS = FtpPathRepository
