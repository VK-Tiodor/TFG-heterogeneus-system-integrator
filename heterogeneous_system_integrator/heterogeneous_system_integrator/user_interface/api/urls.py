from rest_framework.routers import DefaultRouter

from heterogeneous_system_integrator.user_interface.api.viewset import *
from heterogeneous_system_integrator.domain import *


router = DefaultRouter(trailing_slash=False)
router.register(r'api-connections/?', ApiConnectionViewset, ApiConnection._meta.model_name.lower())
router.register(r'db-connections/?', DbConnectionViewset, DbConnection._meta.model_name.lower())
router.register(r'ftp-connections/?', FtpConnectionViewset, FtpConnection._meta.model_name.lower())
router.register(r'api-data-locations/?', ApiDataLocationViewset, ApiDataLocation._meta.model_name.lower())
router.register(r'db-data-locations/?', DbDataLocationViewset, DbDataLocation._meta.model_name.lower())
router.register(r'ftp-data-locations/?', FtpDataLocationViewset, FtpDataLocation._meta.model_name.lower())
router.register(r'conversions/?', ConversionViewset, Conversion._meta.model_name.lower())
router.register(r'filters/?', FilterViewset, Filter._meta.model_name.lower())
router.register(r'mappings/?', MappingViewset, Mapping._meta.model_name.lower())
router.register(r'api-paths/?', ApiPathViewset, ApiPath._meta.model_name.lower())
router.register(r'db-paths/?', DbPathViewset, DbPath._meta.model_name.lower())
router.register(r'ftp-paths/?', FtpPathViewset, FtpPath._meta.model_name.lower())
router.register(r'transfer-steps/?', TransferStepViewset, TransferStep._meta.model_name.lower())
router.register(r'transform-steps/?', TransformStepViewset, TransformStep._meta.model_name.lower())
router.register(r'subtasks/?', SubtaskViewset, Subtask._meta.model_name.lower())
router.register(r'tasks/?', AsyncTaskViewset, AsyncTask._meta.model_name.lower())
router.register(r'tasks/?', PlannedTaskViewset, PlannedTask._meta.model_name.lower())
router.register(r'tasks/?', PeriodicTaskViewset, PeriodicTask._meta.model_name.lower())
