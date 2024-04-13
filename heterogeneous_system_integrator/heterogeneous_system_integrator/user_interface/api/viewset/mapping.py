from heterogeneous_system_integrator.service.mapping import MappingService
from heterogeneous_system_integrator.user_interface.api.serializer.mapping import MappingSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class MappingViewset(BaseViewset):
    
    SERVICE_CLASS = MappingService
    serializer_class = MappingSerializer
