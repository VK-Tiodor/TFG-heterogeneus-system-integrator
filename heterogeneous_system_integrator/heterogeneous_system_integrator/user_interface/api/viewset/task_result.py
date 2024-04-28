from heterogeneous_system_integrator.service.task_result import TaskResultService
from heterogeneous_system_integrator.user_interface.api.serializer.task_result import TaskResultSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class TaskResultViewset(BaseViewset):
    
    SERVICE_CLASS = TaskResultService
    serializer_class = TaskResultSerializer
    