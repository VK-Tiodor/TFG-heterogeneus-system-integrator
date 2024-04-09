from django.apps import AppConfig
from heterogeneous_system_integrator.settings import MAIN_APP_NAME, MAIN_APP_VERBOSE


class HeterogeneousSystemIntegratorConfig(AppConfig):
    name = MAIN_APP_NAME
    verbose_name = MAIN_APP_VERBOSE
