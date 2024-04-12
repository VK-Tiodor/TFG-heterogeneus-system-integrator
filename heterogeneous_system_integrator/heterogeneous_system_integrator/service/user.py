from django.contrib.auth import login

from heterogeneous_system_integrator.repository.user import UserRepository
from heterogeneous_system_integrator.service.base import BaseService


class UserService(BaseService):
    REPOSITORY_CLASS = UserRepository

    @classmethod
    def force_admin_login(cls, request):
        user = cls.REPOSITORY_CLASS.get_or_create(
            username='admin',
            default_properties={
                'is_staff': True, 
                'is_superuser': True,
                'password': 'default_password',
            }
        )
        login(request, user)
