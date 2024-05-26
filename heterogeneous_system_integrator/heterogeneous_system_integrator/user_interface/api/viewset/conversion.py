from heterogeneous_system_integrator.service.conversion import ConversionService
from heterogeneous_system_integrator.user_interface.api.serializer.conversion import ConversionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseConversionViewset:
    SERVICE_CLASS = ConversionService


class ConversionViewset(_BaseConversionViewset, BaseViewset):
    serializer_class = ConversionSerializer


class ConversionAdminViewset(_BaseConversionViewset, BaseAdminViewset):
    pass
