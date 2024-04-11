from django.db.models.fields import related, reverse_related
from django.contrib.admin import AdminSite, ModelAdmin
from django.utils.translation import gettext as _

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
    Filter, 
    Mapping,
    Subtask, 
    Task,
    TransferStep,
    TransformStep,
]
for model in models_to_register:
    class MyAdminModel(ModelAdmin):
        list_display = [
            field.name for field in model._meta.get_fields() 
            if not isinstance(field, (related.RelatedField, reverse_related.ForeignObjectRel)) 
        ]
    
    admin_site.register(model, MyAdminModel)
