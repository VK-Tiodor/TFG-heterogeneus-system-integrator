from django.contrib import admin
from django.utils.translation import gettext as _

from heterogeneous_system_integrator.domain import *
from heterogeneous_system_integrator.service.user import UserService
from heterogeneous_system_integrator.settings import MAIN_APP_VERBOSE, CELERY_MONITOR_HOST
from heterogeneous_system_integrator.user_interface.api.viewset import *


class MyAdminSite(admin.AdminSite):
    index_template = 'index.html'
    app_index_template = 'app_index.html'
    # Text to put at the end of each page's <title>.
    site_title = _(f'{MAIN_APP_VERBOSE} | Administration')
    # Text to put in each page's <h1> (and above login form).
    site_header = _(f'{MAIN_APP_VERBOSE}')
    # Text to put at the top of the admin index page.
    index_title = _('Administration')

    def each_context(self, request):
        context = super().each_context(request)
        context['monitor_url'] = CELERY_MONITOR_HOST
        return context
    
    # No user system implemented
    def login(self, request, extra_context=None):
        if not request.user.pk:
            UserService.force_admin_login(request)
        return super().login(request, extra_context)


admin_site = MyAdminSite()
models_and_admin_viewsets = [
    (ApiConnection, ApiConnectionAdminViewset),
    (ApiDataLocation, ApiDataLocationAdminViewset),
    (Conversion, ConversionAdminViewset),
    (DbConnection, DbConnectionAdminViewset),
    (DbDataLocation, DbDataLocationAdminViewset),
    (Filter, FilterAdminViewset),
    (FtpConnection, FtpConnectionAdminViewset),
    (FtpDataLocation, FtpDataLocationAdminViewset),
    (Mapping, MappingAdminViewset),
    (Period, PeriodAdminViewset),
    (PeriodicTask, PeriodicTaskAdminViewset),
    (PlannedTask, PlannedTaskAdminViewset),
    (Subtask, SubtaskAdminViewset),
    (TaskResult, TaskResultAdminViewset),
    (TransferStep, TransferStepAdminViewset),
    (TransformStep, TransformStepAdminViewset),
    (AsyncTask, AsyncTaskAdminViewset),
]
for model, admin_viewset in models_and_admin_viewsets:
    admin_site.register(model, admin_viewset)
