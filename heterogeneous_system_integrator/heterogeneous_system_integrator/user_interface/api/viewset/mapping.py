from heterogeneous_system_integrator.service.mapping import MappingService
from heterogeneous_system_integrator.user_interface.api.serializer.mapping import MappingSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseMappingViewset:
    SERVICE_CLASS = MappingService


class MappingViewset(_BaseMappingViewset, BaseViewset):
    serializer_class = MappingSerializer


class MappingAdminViewset(_BaseMappingViewset, BaseAdminViewset):
    pass