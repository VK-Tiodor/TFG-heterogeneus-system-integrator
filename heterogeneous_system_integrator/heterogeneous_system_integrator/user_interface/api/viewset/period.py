from heterogeneous_system_integrator.service.period import PeriodService
from heterogeneous_system_integrator.user_interface.api.serializer.period import PeriodSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class PeriodViewset(BaseViewset):
    
    SERVICE_CLASS = PeriodService
    serializer_class = PeriodSerializer
    