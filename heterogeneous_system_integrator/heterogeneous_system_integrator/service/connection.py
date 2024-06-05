from base64 import b64encode
from datetime import datetime
from ftplib import FTP
from io import BufferedReader, BufferedWriter
from time import time
import os

from celery import states
import requests

from heterogeneous_system_integrator.domain.connection import (
    BaseConnection, ApiConnection, DbConnection, FtpConnection, API_AUTH_TYPE_BASIC, API_AUTH_TYPE_KEY, API_TYPE_REST
)
from heterogeneous_system_integrator.repository.connection import (
    BaseConnectionRepository, ApiConnectionRepository, DbConnectionRepository, FtpConnectionRepository
)
from heterogeneous_system_integrator.service.base import BaseService


def batch_processor(data: list[dict]):
    batch_size = 200
    for batch in [data[init_pos:init_pos+batch_size] for init_pos in range(0, len(data), batch_size)]:
        yield batch


class BaseConnectionService(BaseService):
    REPOSITORY_CLASS: BaseConnectionRepository = None

    @classmethod
    def get_password(cls, model: BaseConnection):
        return cls.REPOSITORY_CLASS.get_password(model)


class ApiConnectionService(BaseConnectionService):
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
    def download_data(cls, url: str, headers: dict) -> tuple[list[dict] | dict, dict]:
        data = []
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        init_time = time()
        response = requests.get(url=url, headers=headers)
        try:
            response.raise_for_status()
        except Exception as ex:
            exec_data['errors'] = 1
            exec_time = round((time() - init_time) * 1000, 2)
            exec_data['logs'] = [f'{exec_time}ms > {str(ex)}']
            exec_data['status'] = states.FAILURE
        else:
            data = response.json()
            exec_data['status'] = states.SUCCESS

        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return data, exec_data

    @classmethod
    def upload_data(cls, url: str, headers: dict, data: list[dict]) -> dict:
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        init_time = time()
        for i, batch in enumerate(batch_processor(data), start=1):
            response = requests.post(url=url, headers=headers, data=data)
            try:
                response.raise_for_status()
            except Exception as ex:
                exec_data['errors'] += 1
                exec_time = round((time() - init_time) * 1000, 2)
                exec_data['logs'] += [f'{exec_time}ms > {str(ex)}']

        exec_data['status'] = states.SUCCESS if not exec_data['errors'] else states.FAILURE
        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return exec_data
        
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
class DbConnectionService(BaseConnectionService):
    REPOSITORY_CLASS = DbConnectionRepository

    @classmethod
    def download_data(cls, connection: DbConnection, *args, **kwargs) -> tuple[list[dict] | dict, dict]:
        pass


# TODO
class FtpConnectionService(BaseConnectionService):
    REPOSITORY_CLASS = FtpConnectionRepository

    @classmethod
    def download_data(cls, connection: FtpConnection, *args, **kwargs) -> tuple[list[dict] | dict, dict]:
        pass

    @classmethod
    def _get_ftp_filename(cls, file: BufferedReader) -> str:
        timestamp = datetime.now().strftime('%d%m%Y%H%M%S%f')
        filename, extension = os.path.basename(file.name).split('.')
        return f'{filename}-{timestamp}.{extension}'

    @classmethod
    def _go_to_directory(cls, connection: FTP, path: list[str]):
        for directory in path:
            if directory not in connection.nlst():
                connection.mkd(directory)

            connection.cwd(directory)

    @classmethod
    def _transfer_through_default_connection(cls, host: str, user: str, passwd: str, path: list[str], file: BufferedReader):
        with FTP(host, user, passwd) as connection:
            cls._go_to_directory(connection, path)
            connection.storbinary(f'STOR {cls._get_ftp_filename(file)}', file)

    @classmethod
    def _transfer_through_custom_port_connection(cls, host, user, passwd, port, path: list[str], file: BufferedReader):
        connection = FTP()
        connection.connect(host, port)
        connection.login(user, passwd)
        cls._go_to_directory(connection, path)
        connection.storbinary(f'STOR {cls._get_ftp_filename(file)}', file)

        if connection.sock is not None:
            connection.quit()

    @classmethod
    def upload_data(cls, connection: FtpConnection, path: list[str], file: BufferedReader) -> dict:
        host = connection.hostname
        user = connection.username
        passwd = cls.get_password(connection)
        port = connection.port
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        init_time = time()
        try:
            if not port:
                cls._transfer_through_default_connection(host, user, passwd, path, file)
            else:
                cls._transfer_through_custom_port_connection(host, user, passwd, port, path, file)
        except Exception as ex:
            exec_data['errors'] = 1
            exec_time = round((time() - init_time) * 1000, 2)
            exec_data['logs'] = [f'{exec_time}ms > {str(ex)}']
            exec_data['status'] = states.FAILURE
        else:
            exec_data['status'] = states.SUCCESS

        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return exec_data
