from heterogeneous_system_integrator.repository.base import BaseRepository
from django.contrib.auth.models import User


class UserRepository(BaseRepository):
    MODEL_CLASS = User
