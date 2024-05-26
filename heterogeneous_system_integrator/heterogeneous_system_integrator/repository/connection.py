from base64 import b64encode

from cryptography.fernet import Fernet
from django.db import IntegrityError

from heterogeneous_system_integrator.domain.base import BaseConnection
from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection, API_AUTH_TYPES, API_AUTH_TYPE_BEARER
from heterogeneous_system_integrator.repository.base import BaseRepository
from heterogeneous_system_integrator.settings import SECRET_KEY


class BaseConnectionRepository(BaseRepository):
    ENCRYPTOR = Fernet(b64encode(SECRET_KEY.encode("utf-8")))

    @classmethod
    def _encrypt_password(cls, password: str):
        return cls.ENCRYPTOR.encrypt(password.encode())
    
    @classmethod
    def _decrypt_password(cls, password: str):
        return cls.ENCRYPTOR.decrypt(password)
    
    @classmethod
    def _pre_save_model_operations(cls, model: BaseConnection):
        if model.password:
            model.password = cls._encrypt_password(model.password)
        super()._pre_save_model_operations(model)

    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[BaseConnection], fields: list[str] = None):
        for model in models:
            if model.password:
                model.password = cls._encrypt_password(model.password)
        super()._pre_save_multiple_models_operations(models, fields)

    @classmethod
    def get_password(cls, model: BaseConnection):
        return cls._decrypt_password(model.password)
        

class ApiConnectionRepository(BaseConnectionRepository):
    MODEL_CLASS = ApiConnection

    @classmethod
    def _validate_fields(cls, model: ApiConnection):
        if (model.username or model.password):
            if not (model.auth_endpoint and model.auth_type):
                raise IntegrityError(f'"Auth endpoint" and "Auth type" must be fulfilled when API requires to be logged.')
            if model.auth_type == API_AUTH_TYPE_BEARER and not (model.access_token_field_name and model.username_field_name and model.password_field_name):
                raise IntegrityError(f'"Access token field name", "Username field name" and "Password field name" must be fulfilled when auth type is {API_AUTH_TYPES[API_AUTH_TYPE_BEARER]}')    

    @classmethod
    def _pre_save_model_operations(cls, model: ApiConnection):
        cls._validate_fields(model)
        super()._pre_save_model_operations(model)

    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[ApiConnection], fields: list[str] = None):
        for model in models:
            cls._validate_fields(cls, model)
        super()._pre_save_multiple_models_operations(models, fields)


class DbConnectionRepository(BaseConnectionRepository):
    MODEL_CLASS = DbConnection


class FtpConnectionRepository(BaseConnectionRepository):
    MODEL_CLASS = FtpConnection
