from heterogeneous_system_integrator.service.step import TransferStepService, TransformStepService
from heterogeneous_system_integrator.user_interface.api.serializer.step import TransferStepSerializer, TransformStepSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseTransferStepViewset:
    SERVICE_CLASS = TransferStepService


class TransferStepViewset(_BaseTransferStepViewset, BaseViewset):
    serializer_class = TransferStepSerializer


class TransferStepAdminViewset(_BaseTransferStepViewset, BaseAdminViewset):
    pass


class _BaseTransformStepViewset:
    SERVICE_CLASS = TransformStepService


class TransformStepViewset(_BaseTransformStepViewset, BaseViewset):
    serializer_class = TransformStepSerializer


class TransformStepAdminViewset(_BaseTransformStepViewset, BaseAdminViewset):
    pass
