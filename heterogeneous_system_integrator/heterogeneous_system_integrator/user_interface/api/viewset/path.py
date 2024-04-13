from heterogeneous_system_integrator.service.path import ApiPathService, DbPathService, FtpPathService
from heterogeneous_system_integrator.user_interface.api.serializer.path import ApiPathSerializer, DbPathSerializer, FtpPathSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class ApiPathViewset(BaseViewset):
    
    SERVICE_CLASS = ApiPathService
    serializer_class = ApiPathSerializer


class DbPathViewset(BaseViewset):
    
    SERVICE_CLASS = DbPathService
    serializer_class = DbPathSerializer


class FtpPathViewset(BaseViewset):
    
    SERVICE_CLASS = FtpPathService
    serializer_class = FtpPathSerializer
