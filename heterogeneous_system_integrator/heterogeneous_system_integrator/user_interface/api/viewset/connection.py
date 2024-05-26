from heterogeneous_system_integrator.service.connection import ApiConnectionService, DbConnectionService, FtpConnectionService
from heterogeneous_system_integrator.user_interface.api.serializer.connection import ApiConnectionSerializer, DbConnectionSerializer, FtpConnectionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseApiConnectionViewset:
    SERVICE_CLASS = ApiConnectionService


class ApiConnectionViewset(_BaseApiConnectionViewset, BaseViewset):
    serializer_class = ApiConnectionSerializer


class ApiConnectionAdminViewset(_BaseApiConnectionViewset, BaseAdminViewset):
    pass


class _BaseDbConnectionViewset:
    SERVICE_CLASS = DbConnectionService


class DbConnectionViewset(_BaseDbConnectionViewset, BaseViewset):
    serializer_class = DbConnectionSerializer


class DbConnectionAdminViewset(_BaseDbConnectionViewset, BaseAdminViewset):
    pass


class _BaseFtpConnectionViewset:
    SERVICE_CLASS = FtpConnectionService


class FtpConnectionViewset(_BaseFtpConnectionViewset, BaseViewset):
    serializer_class = FtpConnectionSerializer


class FtpConnectionAdminViewset(_BaseFtpConnectionViewset, BaseAdminViewset):
    pass
