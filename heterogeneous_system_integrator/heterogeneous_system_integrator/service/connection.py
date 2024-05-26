from base64 import b64encode
from json import dumps

import requests

from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection, API_AUTH_TYPE_BASIC, API_AUTH_TYPE_KEY, API_TYPE_REST
from heterogeneous_system_integrator.repository.connection import ApiConnectionRepository, DbConnectionRepository, FtpConnectionRepository
from heterogeneous_system_integrator.service.base import BaseService


def batch_processor(data: list[dict]):
    batch_size = 200
    for batch in [data[init_pos:init_pos+batch_size] for init_pos in range(0, len(data), batch_size)]:
        yield batch


class ApiConnectionService(BaseService):
    REPOSITORY_CLASS = ApiConnectionRepository

    @classmethod
    def build_full_url(cls, connection: ApiConnection, endpoint: str) -> str:
        base_url = connection.hostname

        if base_url.endswith('/'):
            base_url = base_url[:-1]

        if endpoint.startswith('/'):
            endpoint = endpoint[1:]

        return f'{base_url}/{endpoint}'

    @classmethod
    def download_data(cls, url: str, headers: dict) -> list[dict] | dict:
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            try:
                response.raise_for_status()
            
            except Exception as ex:
                raise TypeError(f'Data download process failed. Reason: {str(ex)}')
        
        data = response.json()
        return data

    @classmethod
    def upload_data(cls, url: str, headers: dict, data: list[dict]) -> list[str]:
        responses = []
        for batch in batch_processor(data):
            response = requests.post(url=url, headers=headers, data=data)

            if not response.ok:
                try:
                    response.raise_for_status()
                
                except Exception as ex:
                    responses += [f'Data upload process failed. Reason: {str(ex)}']
                
            responses += [dumps(response.json(), indent=2)]
        
        return responses
        
    @classmethod
    def build_headers(cls, connection: ApiConnection) -> dict:
        if connection.api_type == API_TYPE_REST:
            headers = {
                'Accept': 'application/json',
                'Content-type': 'application/json',
            }
        
        else:
            headers = {
                'Accept': 'application/xml',
                'Content-type': 'application/xml',
            }
        
        headers = cls._authenticate(connection, headers)
        return headers

    @classmethod
    def _authenticate(cls, connection: ApiConnection, headers: dict) -> dict:
        if not (connection.username or connection.password):
            return headers
        
        passwd = cls.REPOSITORY_CLASS.get_password(connection)

        if connection.auth_type == API_AUTH_TYPE_BASIC:
            auth = {'Authorization': f'Basic {b64encode(f"{connection.username}:{passwd}".encode("utf-8")).decode("ascii")}'}
        
        elif connection.auth_type == API_AUTH_TYPE_KEY:
            auth = {'x-api-key': b64encode(passwd.encode("utf-8")).decode("ascii")}
        
        else:
            login = {
                connection.username_field_name: connection.user,
                connection.password_field_name: b64encode(passwd.encode("utf-8")).decode("ascii")
            }
            response = requests.post(
                cls.build_full_url(connection, connection.auth_endpoint),
                headers=headers,
                data=login
            )
            
            if not response.ok:
                try:
                    response.raise_for_status()
                
                except Exception as ex:
                    raise TypeError(f'Login request failed. Reason: {str(ex)}')
                
            access_token = response.json[connection.access_token_field_name]
            auth = {'Authorization': f'Bearer {access_token}'}
        
        headers.update(auth)
        return headers


# TODO
class DbConnectionService(BaseService):
    REPOSITORY_CLASS = DbConnectionRepository

    @classmethod
    def download_data(cls, connection: DbConnection, *args, **kwargs):
        pass


# TODO
class FtpConnectionService(BaseService):
    REPOSITORY_CLASS = FtpConnectionRepository

    @classmethod
    def download_data(cls, connection: FtpConnection, *args, **kwargs):
        pass
