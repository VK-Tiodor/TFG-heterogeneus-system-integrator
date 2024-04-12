from django.db import models

from heterogeneous_system_integrator.domain.base import Base


class ApiPath(Base):
    endpoint = models.CharField()
    path_to_results_list = models.CharField(null=True, blank=True)


class DbPath(Base):
    name = models.CharField()
    schema = models.CharField()
    table = models.CharField()


class FtpPath(Base):
    path_to_files = models.CharField()
    filename_or_regex_pattern = models.CharField(null=True, blank=True)