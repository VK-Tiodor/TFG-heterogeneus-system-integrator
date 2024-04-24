from django.db import models, IntegrityError

from heterogeneous_system_integrator.domain.base import Base, BaseConnection

API_TYPES = {
    (API_TYPE_SOAP := 'soap'): 'SOAP',
    (API_TYPE_REST := 'rest'): 'REST',
}

API_AUTH_TYPES = {
    (API_AUTH_TYPE_BASIC := 'basic'): 'Basic',
    (API_AUTH_TYPE_BEARER := 'bearer'): 'Bearer',
    (API_AUTH_TYPE_KEY := 'key'): 'X-Api-Key',
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
    auth_endpoint = models.CharField(null=True, blank=True)
    auth_type = models.CharField(choices=list(API_AUTH_TYPES.items()), null=True, blank=True, help_text='Authentication method. Leave blank if no login is required to use the API')
    username_field_name = models.CharField(null=True, blank=True, help_text=f'Field name of the username that goes in the login request. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_BEARER]}')
    password_field_name = models.CharField(null=True, blank=True, help_text=f'Field name of the password that goes in the login request. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_BEARER]}')
    access_token_field_name = models.CharField(null=True, blank=True, help_text=f'Field name of the access token that comes in the login response. Leave blank if auth type is not {API_AUTH_TYPES[API_AUTH_TYPE_BEARER]}')
    api_type = models.CharField(choices=list(API_TYPES.items()))

    def save(self, *args, **kwargs):
        if (self.username or self.password):
            if not (self.auth_endpoint and self.auth_type):
                raise IntegrityError(f'Auth endpoint and Auth type must be fulfilled when API requires to be logged.')
            if self.auth_type == API_AUTH_TYPE_BEARER and not (self.access_token_field_name and self.username_field_name and self.password_field_name):
                raise IntegrityError(f'Access token field name, Username field name and Password field name must be fulfilled when auth type is {API_AUTH_TYPES[API_AUTH_TYPE_BEARER]}')
        return super().save(*args, **kwargs)


class DbConnection(Base, BaseConnection):
    db_type = models.CharField(choices=list(DB_TYPES.items()))


class FtpConnection(Base, BaseConnection):
    ftp_type = models.CharField(choices=list(FTP_TYPES.items()))
