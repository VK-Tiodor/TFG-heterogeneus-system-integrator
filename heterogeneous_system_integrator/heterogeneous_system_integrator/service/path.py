from heterogeneous_system_integrator.repository.path import ApiPathRepository, DbPathRepository, FtpPathRepository
from heterogeneous_system_integrator.service.base import BaseService


class ApiPathService(BaseService):
    REPOSITORY_CLASS = ApiPathRepository


class DbPathService(BaseService):
    REPOSITORY_CLASS = DbPathRepository


class FtpPathService(BaseService):
    REPOSITORY_CLASS = FtpPathRepository
