from django.db.models.fields import related, reverse_related
from django.contrib.admin import AdminSite, ModelAdmin
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _
from django_celery_results.models import TaskResult

from heterogeneous_system_integrator.domain import *
from heterogeneous_system_integrator.service import *
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
models_and_services=[
    (ApiConnection, ApiConnectionService),
    (ApiDataLocation, ApiDataLocationService),
    (ApiPath, ApiPathService),
    (AsyncTask, AsyncTaskService),
    (Conversion, ConversionService),
    (DbConnection, DbConnectionService),
    (DbDataLocation, DbDataLocationService),
    (DbPath, DbPathService),
    (Filter, FilterService), 
    (FtpConnection, FtpConnectionService),
    (FtpDataLocation, FtpDataLocationService),
    (FtpPath, FtpPathService),
    (Mapping, MappingService),
    (Period, PeriodService),
    (PeriodicTask, PeriodicTaskService),
    (PlannedTask, PlannedTaskService),
    (Subtask, SubtaskService), 
    (TaskResult, TaskResultService),
    (TransferStep, TransferStepService),
    (TransformStep, TransformStepService),
]

for model, service in models_and_services:
    class MyAdminModel(ModelAdmin):

        def get_list_display(self, request) -> list:
            return [
                field.name for field in model._meta.get_fields() 
                if not isinstance(field, (related.RelatedField, reverse_related.ForeignObjectRel)) and field.name != 'slug'
            ]
        
        def get_queryset(self, request) -> QuerySet:
            return service.create_query(order_by=['name'])
        
        def get_search_results(self, request, queryset, search_term) -> tuple[QuerySet, bool]:
            duplicates = False
            try:
                search_term = int(search_term)
                return service.create_query(filters={'pk': search_term}, order_by=['name']), duplicates
            except Exception:
                return service.create_query(filters={'name__icontains': search_term}, order_by=['name']), duplicates

        def save_model(self, request, obj, form, change) -> None:
            if not change:
                return service.insert(model=obj)
            else:
                return service.update(model=obj)
        
        def delete_model(request, obj) -> None:
            return service.delete(model=obj)
        
        def delete_queryset(self, request, queryset) -> None:
            return service.delete(query=queryset)

    admin_site.register(model, MyAdminModel)
