from django.db import models

from heterogeneous_system_integrator.domain.base import Base


class ApiPath(Base):
    endpoint = models.CharField(help_text='API Endpoint where to apply the requests')
    path_to_results_list = models.CharField(null=True, blank=True, help_text='Path to the results list from where to get data. Separate field names using dots (.)')


class DbPath(Base):
    name = models.CharField(help_text='Database name')
    schema = models.CharField(help_text='Schema name')
    table = models.CharField(help_text='Table name')


class FtpPath(Base):
    path_to_files = models.CharField(help_text='Path to the folder where the transfering file process is going to take place. Separate field names using slashes (/)')
    filename_or_regex_pattern = models.CharField(null=True, blank=True, help_text='Filename or regular expression for multiple files from where to get data')
