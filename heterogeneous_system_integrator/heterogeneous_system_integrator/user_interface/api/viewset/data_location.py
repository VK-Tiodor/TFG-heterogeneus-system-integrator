from heterogeneous_system_integrator.service.data_location import ApiDataLocationService, DbDataLocationService, FtpDataLocationService
from heterogeneous_system_integrator.user_interface.api.serializer.data_location import ApiDataLocationSerializer, DbDataLocationSerializer, FtpDataLocationSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class ApiDataLocationViewset(BaseViewset):
    
    SERVICE_CLASS = ApiDataLocationService
    serializer_class = ApiDataLocationSerializer


class DbDataLocationViewset(BaseViewset):
    
    SERVICE_CLASS = DbDataLocationService
    serializer_class = DbDataLocationSerializer


class FtpDataLocationViewset(BaseViewset):
    
    SERVICE_CLASS = FtpDataLocationService
    serializer_class = FtpDataLocationSerializer
