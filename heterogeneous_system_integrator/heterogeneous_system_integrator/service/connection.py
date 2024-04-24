from base64 import b64encode

from cryptography.fernet import Fernet
import requests

from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection, API_AUTH_TYPE_BASIC, API_AUTH_TYPE_KEY, API_TYPE_REST
from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath
from heterogeneous_system_integrator.repository.connection import ApiConnectionRepository, DbConnectionRepository, FtpConnectionRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.path import ApiPathService
from heterogeneous_system_integrator.settings import SECRET_KEY


def batch_processor(cls, data: list[dict]):
    batch_size = 200
    for batch in [data[init_pos:init_pos+batch_size] for init_pos in range(0, len(data), batch_size)]:
        yield batch


class ApiConnectionService(BaseService):
    MODEL_CLASS = ApiConnectionRepository

    @classmethod
    def download_data(cls, url: str, headers: dict) -> list[dict]:
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            try:
                response.raise_for_status()
            except Exception as ex:
                raise TypeError(f'Data download process failed. Reason: {str(ex)}')
        data = response.json
        return data

    @classmethod
    def upload_data(cls, url: str, headers: dict, data: list[dict]):
        for batch in batch_processor(data):
            response = requests.post(url=url, headers=headers, data=data)

            if not response.ok:
                try:
                    response.raise_for_status()
                except Exception as ex:
                    raise TypeError(f'Data upload process failed. Reason: {str(ex)}')
        
    @classmethod
    def build_headers(cls, connection: ApiConnection) -> dict:
        if connection.api_type == API_TYPE_REST:
            headers =  {
                'Accept' : 'application/json',
                'Content-type' : 'application/json',
            }
        else:
            headers = {
                'Accept' : 'application/xml',
                'Content-type' : 'application/xml',
            }
        headers = cls._authenticate(connection, headers)
        return headers

    @classmethod
    def _authenticate(cls, connection: ApiConnection, headers: dict) -> dict:
        if not (connection.username or connection.password):
            return headers
        
        decryptor = Fernet(SECRET_KEY.encode())
        passwd = decryptor.decrypt(connection.password)

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
                ApiPathService.build_full_url(connection.hostname, connection.auth_endpoint),
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
    

class DbConnectionService(BaseService):
    MODEL_CLASS = DbConnectionRepository

    @classmethod
    def download_data(cls, connection: DbConnection, path: DbPath):
        pass


class FtpConnectionService(BaseService):
    MODEL_CLASS = FtpConnectionRepository

    @classmethod
    def download_data(cls, connection: FtpConnection, path: FtpPath):
        pass
