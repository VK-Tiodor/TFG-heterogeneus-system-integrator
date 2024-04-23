from heterogeneous_system_integrator.service.connection import ApiConnectionService, DbConnectionService, FtpConnectionService
from heterogeneous_system_integrator.user_interface.api.serializer.connection import ApiConnectionSerializer, DbConnectionSerializer, FtpConnectionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class ApiConnectionViewset(BaseViewset):
    
    SERVICE_CLASS = ApiConnectionService
    serializer_class = ApiConnectionSerializer


class DbConnectionViewset(BaseViewset):
    
    SERVICE_CLASS = DbConnectionService
    serializer_class = DbConnectionSerializer


class FtpConnectionViewset(BaseViewset):
    
    SERVICE_CLASS = FtpConnectionService
    serializer_class = FtpConnectionSerializer
