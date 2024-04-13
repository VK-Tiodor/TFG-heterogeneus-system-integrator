from heterogeneous_system_integrator.service.conversion import ConversionService
from heterogeneous_system_integrator.user_interface.api.serializer.conversion import ConversionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class ConversionViewset(BaseViewset):
    
    SERVICE_CLASS = ConversionService
    serializer_class = ConversionSerializer
