"""
URL configuration for Heterogeneous_system_integrator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.shortcuts import redirect

from heterogeneous_system_integrator.service.user import UserService
from heterogeneous_system_integrator.user_interface.admin_site import admin_site
from heterogeneous_system_integrator.user_interface.api.urls import router

ADMIN_PATH = 'admin/'
API_PATH = 'api/'

def redirect_to_admin_site_urls(request):
    UserService.force_admin_login(request)
    return redirect(ADMIN_PATH)

urlpatterns = [
    path("", redirect_to_admin_site_urls),
    path(ADMIN_PATH, admin_site.urls),
    path(API_PATH, router.urls)
]
