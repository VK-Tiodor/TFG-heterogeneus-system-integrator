from heterogeneous_system_integrator.service.connection import ConnectionService
from heterogeneous_system_integrator.user_interface.api.serializer.connection import ConnectionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class ConnectionViewset(BaseViewset):
    
    SERVICE_CLASS = ConnectionService
    serializer_class = ConnectionSerializer
