from django.db import models

from heterogeneous_system_integrator.domain.base import Base, BaseConnection

API_TYPES = {
    (API_TYPE_SOAP := 'soap'): 'SOAP',
    (API_TYPE_REST := 'rest'): 'REST',
}

API_AUTH_TYPES = {
    (API_AUTH_TYPE_BASIC := 'basic'): 'Basic',
    (API_AUTH_TYPE_JWT := 'jwt'): 'JWT',
    (API_AUTH_TYPE_KEY := 'key'): 'Api key',
    (API_AUTH_TYPE_OAUTH := 'oauth'): 'OAuth',
}

DB_TYPES = {
    (DB_TYPE_POSTGRES := 'postgres'): 'PostgreSQL',
    (DB_TYPE_MONGO := 'mongo'): 'MongoDB',
}

FTP_TYPES = {
    (FTP_TYPE_BASIC := 'basic'): 'Basic',
    (FTP_TYPE_FTPS := 'ftps'): 'FTPS',
    (FTP_TYPE_FTPES := 'ftpes'): 'FTPES',
    (FTP_TYPE_SFTP := 'sftp'): 'SFTP',
}


class ApiConnection(Base, BaseConnection):
    username_field_name = models.CharField(null=True, blank=True, help_text=f'Field name of the username that goes in the login request. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_JWT]} or {API_AUTH_TYPES[API_AUTH_TYPE_OAUTH]}')
    password_field_name = models.CharField(null=True, blank=True, help_text=f'Field name of the password that goes in the login request. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_JWT]} or {API_AUTH_TYPES[API_AUTH_TYPE_OAUTH]}')
    access_token_field_name = models.CharField(null=True, blank=True, help_text='Field name of the access token that comes in the login response. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_JWT]} or {API_AUTH_TYPES[API_AUTH_TYPE_OAUTH]}')
    auth_endpoint = models.CharField(null=True, blank=True)
    auth_in_payload = models.BooleanField(null=True, blank=True, help_text='Login data is sent in the payload of the request. By default the login information is sent in the headers of the request')
    auth_type = models.CharField(choices=list(API_AUTH_TYPES.items()), null=True, blank=True, help_text='Authentication method. Leave blank if no login is required to use the API')
    api_type = models.CharField(choices=list(API_TYPES.items()))


class DbConnection(Base, BaseConnection):
    db_type = models.CharField(choices=list(DB_TYPES.items()))


class FtpConnection(Base, BaseConnection):
    ftp_type = models.CharField(choices=list(FTP_TYPES.items()))
