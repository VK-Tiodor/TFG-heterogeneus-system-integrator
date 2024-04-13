from heterogeneous_system_integrator.service.step import TransferStepService, TransformStepService
from heterogeneous_system_integrator.user_interface.api.serializer.step import TransferStepSerializer, TransformStepSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset


class TransferStepViewset(BaseViewset):
    
    SERVICE_CLASS = TransferStepService
    serializer_class = TransferStepSerializer


class TransformStepViewset(BaseViewset):
    
    SERVICE_CLASS = TransformStepService
    serializer_class = TransformStepSerializer
