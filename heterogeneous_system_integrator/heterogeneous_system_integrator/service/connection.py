from base64 import b64encode

from cryptography.fernet import Fernet
import requests

from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection, API_AUTH_TYPE_BASIC, API_AUTH_TYPE_KEY, API_TYPE_REST
from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath
from heterogeneous_system_integrator.repository.connection import ApiConnectionRepository, DbConnectionRepository, FtpConnectionRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.path import ApiPathService
from heterogeneous_system_integrator.settings import SECRET_KEY


class ApiConnectionService(BaseService):
    MODEL_CLASS = ApiConnectionRepository

    @classmethod
    def download_data(cls, url: str, headers: dict, payload: dict = {}):
        response = requests.get(url=url, headers=headers, data=payload)
        if not response.ok:
            try:
                response.raise_for_status()
            except Exception as ex:
                raise TypeError(f'Login request failed. Reason: {str(ex)}')
        data = response.json
        
    @classmethod
    def prepare_message(cls, connection: ApiConnection) -> tuple[dict, dict]:
        authorization = cls._authenticate(connection)
        if not connection.auth_in_payload:
            headers = cls._build_headers(connection, authorization)
            return headers, {}
        else:
            return headers, authorization

    @classmethod
    def _authenticate(cls, connection: ApiConnection) -> dict:
        if not connection.auth_type:
            return None 
        
        decryptor = Fernet(SECRET_KEY.encode())
        passwd = decryptor.decrypt(connection.password)
        if connection.auth_type == API_AUTH_TYPE_BASIC:
            return {'Authorization': f'Basic {b64encode(f"{connection.username}:{passwd}".encode("utf-8")).decode("ascii")}'}
        
        elif connection.auth_type == API_AUTH_TYPE_KEY:
            return {'x-api-key': b64encode(f"{passwd}".encode("utf-8")).decode("ascii")}
        
        else:
            response = requests.post(
                connection.auth_endpoint,
                {
                    connection.username_field_name: connection.user,
                    connection.password_field_name: b64encode(f"{passwd}".encode("utf-8")).decode("ascii")
                }
            )
            if not response.ok:
                try:
                    response.raise_for_status()
                except Exception as ex:
                    raise TypeError(f'Login request failed. Reason: {str(ex)}')
                
            access_token = response.json[connection.access_token_field_name]
            return {'Authorization': f'Bearer {access_token}'}
    
    @classmethod
    def _build_headers(cls, connection: ApiConnection, authentication: dict = {}) -> dict:
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
        headers.update(authentication)
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
