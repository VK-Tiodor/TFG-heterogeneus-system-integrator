from heterogeneous_system_integrator.service.filter import FilterService
from heterogeneous_system_integrator.user_interface.api.serializer.filter import FilterSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class FilterViewset(BaseViewset):
    
    SERVICE_CLASS = FilterService
    serializer_class = FilterSerializer
