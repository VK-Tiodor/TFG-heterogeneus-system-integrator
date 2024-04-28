from django_celery_results.models import TaskResult

from heterogeneous_system_integrator.repository.base import BaseRepository


class TaskResultRepository(BaseRepository):
    MODEL_CLASS = TaskResult
