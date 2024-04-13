from heterogeneous_system_integrator.service.subtask import SubtaskService
from heterogeneous_system_integrator.user_interface.api.serializer.subtask import SubtaskSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class SubtaskViewset(BaseViewset):
    
    SERVICE_CLASS = SubtaskService
    serializer_class = SubtaskSerializer
