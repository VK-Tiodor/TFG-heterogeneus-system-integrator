from django.db import models

from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection


class BaseDataLocation(Base):
    pass


class ApiDataLocation(BaseDataLocation):
    connection = models.ForeignKey(
        ApiConnection,
        on_delete=models.PROTECT,
        related_name='data_locations',
        help_text='Connection where the transfering data process is going to take place'
    )
    endpoint = models.CharField(help_text='API Endpoint where to apply the requests')
    path_to_results_list = models.CharField(
        null=True,
        blank=True,
        help_text='Path to the results list inside the API response from where to get data. Separate field names using dots (.)'
    )


class DbDataLocation(BaseDataLocation):
    connection = models.ForeignKey(
        DbConnection,
        on_delete=models.PROTECT,
        related_name='data_locations',
        help_text='Connection where the transfering data process is going to take place'
    )
    db_name = models.CharField(help_text='Database name')
    schema = models.CharField(help_text='Schema name')
    table = models.CharField(help_text='Table name')


class FtpDataLocation(BaseDataLocation):
    connection = models.ForeignKey(
        FtpConnection,
        on_delete=models.PROTECT,
        related_name='data_locations',
        help_text='Connection where the transfering data process is going to take place'
    )
    directory_path = models.CharField(
        help_text='Path to the directory where the transfering file process is going to take place. Separate field names using slashes (/)'
    )
    filename = models.CharField(null=True, blank=True, help_text='Filename from where to get or where to save the data')
    regex_pattern = models.CharField(
        null=True,
        blank=True,
        help_text='Regular expression to get data from multiple files'
    )
