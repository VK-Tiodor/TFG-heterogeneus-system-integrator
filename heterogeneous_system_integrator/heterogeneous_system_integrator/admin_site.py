from django.contrib.admin import AdminSite
from django.utils.translation import gettext as _
from django_celery_beat.models import CrontabSchedule
from django_celery_results.models import TaskResult

from heterogeneous_system_integrator.domain.connection import Connection
from heterogeneous_system_integrator.domain.conversion import Conversion
from heterogeneous_system_integrator.domain.filter import Filter
from heterogeneous_system_integrator.domain.mapping import Mapping
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep
from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.domain.task import Task
from heterogeneous_system_integrator.settings import MAIN_APP_VERBOSE


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = _(f'{MAIN_APP_VERBOSE} | Administration')

    # Text to put in each page's <h1> (and above login form).
    site_header = _(f'{MAIN_APP_VERBOSE}')

    # Text to put at the top of the admin index page.
    index_title = _('Administration')


admin_site = MyAdminSite()
models_to_register=[
    Connection,
    Conversion,
    CrontabSchedule,
    Filter, 
    Mapping,
    Subtask, 
    Task,
    TaskResult,
    TransferStep,
    TransformStep,
]
admin_site.register(models_to_register)