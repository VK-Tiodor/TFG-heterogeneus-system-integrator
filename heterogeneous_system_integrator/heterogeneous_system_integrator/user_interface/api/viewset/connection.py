from django import forms
from django.http import HttpRequest

from heterogeneous_system_integrator.service.connection import BaseConnectionService, ApiConnectionService, DbConnectionService, FtpConnectionService
from heterogeneous_system_integrator.domain.connection import BaseConnection, ApiConnection, DbConnection, FtpConnection
from heterogeneous_system_integrator.user_interface.api.serializer.connection import ApiConnectionSerializer, DbConnectionSerializer, FtpConnectionSerializer
from heterogeneous_system_integrator.user_interface.api.viewset.base import BaseViewset, BaseAdminViewset


class _BaseApiConnectionViewset:
    SERVICE_CLASS = ApiConnectionService


class _BaseConnectionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True), required=False)


class _BaseConnectionAdminViewset(BaseAdminViewset):
    SERVICE_CLASS: BaseConnectionService = None

    def get_list_display(self, request: HttpRequest):
        list_display = super().get_list_display(request)
        if 'password' in list_display:
            list_display.pop(list_display.index('password'))
        return list_display


class ApiConnectionViewset(_BaseApiConnectionViewset, BaseViewset):
    serializer_class = ApiConnectionSerializer


class ApiConnectionForm(_BaseConnectionForm):
    class Meta:
        fields = '__all__'
        model = ApiConnection


class ApiConnectionAdminViewset(_BaseApiConnectionViewset, _BaseConnectionAdminViewset):
    form = ApiConnectionForm


class _BaseDbConnectionViewset:
    SERVICE_CLASS = DbConnectionService


class DbConnectionViewset(_BaseDbConnectionViewset, BaseViewset):
    serializer_class = DbConnectionSerializer


class DbConnectionForm(_BaseConnectionForm):
    class Meta:
        fields = '__all__'
        model = DbConnection


class DbConnectionAdminViewset(_BaseDbConnectionViewset, _BaseConnectionAdminViewset):
    form = DbConnectionForm


class _BaseFtpConnectionViewset:
    SERVICE_CLASS = FtpConnectionService


class FtpConnectionViewset(_BaseFtpConnectionViewset, BaseViewset):
    serializer_class = FtpConnectionSerializer


class FtpConnectionForm(_BaseConnectionForm):
    class Meta:
        fields = '__all__'
        model = FtpConnection


class FtpConnectionAdminViewset(_BaseFtpConnectionViewset, _BaseConnectionAdminViewset):
    form = FtpConnectionForm
