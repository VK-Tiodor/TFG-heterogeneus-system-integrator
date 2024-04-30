from django.contrib import messages, admin
from django.db.models.fields import related, reverse_related
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _
from django.utils.text import get_text_list
from django_celery_results.models import TaskResult

from heterogeneous_system_integrator import celery
from heterogeneous_system_integrator.domain import *
from heterogeneous_system_integrator.service import *
from heterogeneous_system_integrator.settings import MAIN_APP_VERBOSE, CELERY_MONITOR_HOST
from heterogeneous_system_integrator.user_interface.api.serializer.task import AsyncTaskSerializer


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
models_and_services=[
    (ApiConnection, ApiConnectionService),
    (ApiDataLocation, ApiDataLocationService),
    (ApiPath, ApiPathService),
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
    (AsyncTask, AsyncTaskService),
]

@admin.action(description='Execute tasks')
def execute_tasks(self, request, queryset):
    task_names = []
    for task in queryset:
        celery.run_async_task.delay(**celery.serialize_task_data(task))
        task_names += [str(task)]
    
    messages.add_message(request, messages.INFO, f'Async tasks {_(get_text_list(task_names, "and"))} {"have" if len(task_names) > 1 else "has"} been queued for execution.')


for model, service in models_and_services:  
    class MyModelAdmin(admin.ModelAdmin):
        SERVICE_CLASS: BaseService = service
        list_display = [
            field.name for field in model._meta.get_fields() 
            if not isinstance(field, (related.RelatedField, reverse_related.ForeignObjectRel)) and field.name != 'slug'
        ]
        actions = [execute_tasks] if model is AsyncTask else []
        
        def get_queryset(self, request) -> QuerySet:
            return self.SERVICE_CLASS.create_query(order_by=['name'])
        
        def get_search_results(self, request, queryset, search_term) -> tuple[QuerySet, bool]:
            duplicates = False
            try:
                search_term = int(search_term)
                return self.SERVICE_CLASS.create_query(filters={'pk': search_term}, order_by=['name']), duplicates
            except Exception:
                return self.SERVICE_CLASS.create_query(filters={'name__icontains': search_term}, order_by=['name']), duplicates

        def save_model(self, request, obj, form, change) -> None:
            if change:
                return self.SERVICE_CLASS.save_model(obj)
            
            relations = {field_name:value for field_name, value in form.cleaned_data.items() if isinstance(value, QuerySet)}
            if not relations:
                return self.SERVICE_CLASS.save_model(obj)
            else:
                return self.SERVICE_CLASS.save_model_with_relations(obj, relations)
        
        def save_related(self, request, form, formsets, change) -> None:
            pass
        
        def delete_model(self, request, obj) -> None:
            return self.SERVICE_CLASS.delete_model(model=obj)
        
        def delete_queryset(self, request, queryset) -> None:
            return self.SERVICE_CLASS.delete_query(query=queryset)
        
        def response_post_save_change(self, request, obj):
            if '_execute' in request.POST:
                celery.run_async_task.delay(**celery.serialize_task_data(obj))
                messages.add_message(request, messages.INFO, f'Async task {str(obj)} has been queued for execution.')
            return super().response_post_save_change(request, obj)
    
    admin_site.register(model, MyModelAdmin)
