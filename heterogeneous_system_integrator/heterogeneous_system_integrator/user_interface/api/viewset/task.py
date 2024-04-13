from heterogeneous_system_integrator.service.task import TaskService
from heterogeneous_system_integrator.user_interface.api.serializer.task import TaskSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class TaskViewset(BaseViewset):
    
    SERVICE_CLASS = TaskService
    serializer_class = TaskSerializer
