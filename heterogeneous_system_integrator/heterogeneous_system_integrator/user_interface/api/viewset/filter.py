from heterogeneous_system_integrator.service.filter import FilterService
from heterogeneous_system_integrator.user_interface.api.serializer.filter import FilterSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseFilterViewset:
    SERVICE_CLASS = FilterService


class FilterViewset(_BaseFilterViewset, BaseViewset):
    serializer_class = FilterSerializer


class FilterAdminViewset(_BaseFilterViewset, BaseAdminViewset):
    pass
