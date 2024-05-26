from heterogeneous_system_integrator.service.data_location import ApiDataLocationService, DbDataLocationService, FtpDataLocationService
from heterogeneous_system_integrator.user_interface.api.serializer.data_location import ApiDataLocationSerializer, DbDataLocationSerializer, FtpDataLocationSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseApiDataLocationViewset:
    SERVICE_CLASS = ApiDataLocationService


class ApiDataLocationViewset(_BaseApiDataLocationViewset, BaseViewset):
    serializer_class = ApiDataLocationSerializer


class ApiDataLocationAdminViewset(_BaseApiDataLocationViewset, BaseAdminViewset):
    pass


class _BaseDbDataLocationViewset:
    SERVICE_CLASS = DbDataLocationService


class DbDataLocationViewset(_BaseDbDataLocationViewset, BaseViewset):
    serializer_class = DbDataLocationSerializer


class DbDataLocationAdminViewset(_BaseDbDataLocationViewset, BaseAdminViewset):
    pass


class _BaseFtpDataLocationViewset:
    SERVICE_CLASS = FtpDataLocationService


class FtpDataLocationViewset(_BaseFtpDataLocationViewset, BaseViewset):
    serializer_class = FtpDataLocationSerializer


class FtpDataLocationAdminViewset(_BaseFtpDataLocationViewset, BaseAdminViewset):
    pass
