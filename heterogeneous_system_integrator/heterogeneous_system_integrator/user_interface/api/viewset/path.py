from heterogeneous_system_integrator.service.path import ApiPathService, DbPathService, FtpPathService
from heterogeneous_system_integrator.user_interface.api.serializer.path import ApiPathSerializer, DbPathSerializer, FtpPathSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseApiPathViewset:
    SERVICE_CLASS = ApiPathService


class ApiPathViewset(_BaseApiPathViewset, BaseViewset):
    serializer_class = ApiPathSerializer


class ApiPathAdminViewset(_BaseApiPathViewset, BaseAdminViewset):
    pass


class _BaseDbPathViewset:
    SERVICE_CLASS = DbPathService


class DbPathViewset(_BaseDbPathViewset, BaseViewset):
    serializer_class = DbPathSerializer


class DbPathAdminViewset(_BaseDbPathViewset, BaseAdminViewset):
    pass


class _BaseFtpPathViewset:
    SERVICE_CLASS = FtpPathService


class FtpPathViewset(_BaseFtpPathViewset, BaseViewset):
    serializer_class = FtpPathSerializer


class FtpPathAdminViewset(_BaseFtpPathViewset, BaseAdminViewset):
    pass
