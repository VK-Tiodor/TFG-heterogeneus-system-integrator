from heterogeneous_system_integrator.service.subtask import SubtaskService
from heterogeneous_system_integrator.user_interface.api.serializer.subtask import SubtaskSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseSubtaskViewset:
    SERVICE_CLASS = SubtaskService


class SubtaskViewset(_BaseSubtaskViewset, BaseViewset):
    serializer_class = SubtaskSerializer


class SubtaskAdminViewset(_BaseSubtaskViewset, BaseAdminViewset):
    pass
