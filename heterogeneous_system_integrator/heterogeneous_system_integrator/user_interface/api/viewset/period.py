from heterogeneous_system_integrator.service.period import PeriodService
from heterogeneous_system_integrator.user_interface.api.serializer.period import PeriodSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BasePeriodViewset:
    SERVICE_CLASS = PeriodService


class PeriodViewset(_BasePeriodViewset, BaseViewset):
    serializer_class = PeriodSerializer


class PeriodAdminViewset(_BasePeriodViewset, BaseAdminViewset):
    pass