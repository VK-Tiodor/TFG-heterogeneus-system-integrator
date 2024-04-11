from django.db import models

from heterogeneous_system_integrator.domain.base import Base


CONNECTION_TYPES = {
    (CONNECTION_TYPE_DB := 'db'): 'Database',
    (CONNECTION_TYPE_FTP := 'ftp'): 'FTP / FTPS / SFTP',
    (CONNECTION_TYPE_API := 'rest'): 'API REST',
}

class Connection(Base):
    type = models.CharField(choices=list(CONNECTION_TYPES.items()))
    hostname = models.CharField(help_text='www.host_site.com or 192.168.0.1')
    port = models.IntegerField(null=True, blank=True, help_text='5432')
    username = models.CharField(null=True, blank=True)
    password = models.CharField(null=True, blank=True)
