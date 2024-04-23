from django.db.models.fields import related, reverse_related
from django.contrib.admin import AdminSite, ModelAdmin
from django.utils.translation import gettext as _
from django_celery_results.models import TaskResult

from heterogeneous_system_integrator.domain import *
from heterogeneous_system_integrator.settings import MAIN_APP_VERBOSE, CELERY_MONITOR_HOST


class MyAdminSite(AdminSite):
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


admin_site = MyAdminSite()
models_to_register=[
    ApiConnection,
    ApiDataLocation,
    ApiPath,
    AsyncTask,
    Conversion,
    DbConnection,
    DbDataLocation,
    DbPath,
    Filter, 
    FtpConnection,
    FtpDataLocation,
    FtpPath,
    Mapping,
    PeriodicTask,
    PlannedTask,
    Subtask, 
    TaskResult,
    TransferStep,
    TransformStep,
]
for model in models_to_register:
    field_names = [
        field.name for field in model._meta.get_fields() 
        if not isinstance(field, (related.RelatedField, reverse_related.ForeignObjectRel)) and field.name != 'slug'
    ]
    class MyAdminModel(ModelAdmin):
        list_display = field_names
    admin_site.register(model, MyAdminModel)
