from rest_framework.routers import DefaultRouter

from heterogeneous_system_integrator.user_interface.api.viewset.connection import ConnectionViewset
from heterogeneous_system_integrator.user_interface.api.viewset.conversion import ConversionViewset
from heterogeneous_system_integrator.user_interface.api.viewset.filter import FilterViewset
from heterogeneous_system_integrator.user_interface.api.viewset.mapping import MappingViewset
from heterogeneous_system_integrator.user_interface.api.viewset.path import ApiPathViewset, DbPathViewset, FtpPathViewset
from heterogeneous_system_integrator.user_interface.api.viewset.step import TransferStepViewset, TransformStepViewset
from heterogeneous_system_integrator.user_interface.api.viewset.subtask import SubtaskViewset
from heterogeneous_system_integrator.user_interface.api.viewset.task import TaskViewset

router = DefaultRouter(trailing_slash=False)
router.register(r'^connections/?', ConnectionViewset)
router.register(r'^conversions/?', ConversionViewset)
router.register(r'^filters/?', FilterViewset)
router.register(r'^mappings/?', MappingViewset)
router.register(r'^api-paths/?', ApiPathViewset)
router.register(r'^db-paths/?', DbPathViewset)
router.register(r'^ftp-paths/?', FtpPathViewset)
router.register(r'^transfer-steps/?', TransferStepViewset)
router.register(r'^transform-steps/?', TransformStepViewset)
router.register(r'^subtasks/?', SubtaskViewset)
router.register(r'^tasks/?', TaskViewset)
