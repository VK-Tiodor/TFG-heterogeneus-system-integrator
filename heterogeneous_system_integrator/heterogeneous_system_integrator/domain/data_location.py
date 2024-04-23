from django.db import models

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection
from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath


class BaseDataLocation(Base):
    pass


class ApiDataLocation(BaseDataLocation):
    connection = models.ForeignKey(ApiConnection, on_delete=models.PROTECT, related_name='data_locations', help_text='Connection where the transfering data process is going to take place')
    path = models.ForeignKey(ApiPath, on_delete=models.PROTECT, related_name='data_locations', help_text='Path to the data in the connection')


class DbDataLocation(BaseDataLocation):
    connection = models.ForeignKey(DbConnection, on_delete=models.PROTECT, related_name='data_locations', help_text='Connection where the transfering data process is going to take place')
    path = models.ForeignKey(DbPath, on_delete=models.PROTECT, related_name='data_locations', help_text='Path to the data in the connection')


class FtpDataLocation(BaseDataLocation):
    connection = models.ForeignKey(FtpConnection, on_delete=models.PROTECT, related_name='data_locations', help_text='Connection where the transfering data process is going to take place')
    path = models.ForeignKey(FtpPath, on_delete=models.PROTECT, related_name='data_locations', help_text='Path to the data in the connection')
