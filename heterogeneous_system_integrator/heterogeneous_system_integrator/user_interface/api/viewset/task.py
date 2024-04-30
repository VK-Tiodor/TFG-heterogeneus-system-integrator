from heterogeneous_system_integrator.service.task import AsyncTaskService, PlannedTaskService, PeriodicTaskService
from heterogeneous_system_integrator.user_interface.api.serializer.task import AsyncTaskSerializer, PlannedTaskSerializer, PeriodicTaskSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


# TODO add execution endpoint

class AsyncTaskViewset(BaseViewset):
    
    SERVICE_CLASS = AsyncTaskService
    serializer_class = AsyncTaskSerializer


class PlannedTaskViewset(BaseViewset):
    
    SERVICE_CLASS = PlannedTaskService
    serializer_class = PlannedTaskSerializer


class PeriodicTaskViewset(BaseViewset):
    
    SERVICE_CLASS = PeriodicTaskService
    serializer_class = PeriodicTaskSerializer
    