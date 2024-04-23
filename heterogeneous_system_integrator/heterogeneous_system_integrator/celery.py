import os

from celery import Celery

from heterogeneous_system_integrator import settings
from heterogeneous_system_integrator.service.task import AsyncTaskService, PlannedTaskService, PeriodicTaskService


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings.__name__)

app = Celery(settings.MAIN_APP_NAME)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings.__name__)

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, name=settings.CELERY_ASYNC_TASK_NAME)
def run_async_task(self, task):
    return AsyncTaskService.run(task)


@app.task(bind=True, name=settings.CELERY_PLANNED_TASK_NAME)
def run_planned_task(self, task):
    return PlannedTaskService.run(task)


@app.task(bind=True, name=settings.CELERY_PERIODIC_TASK_NAME)
def run_periodic_task(self, task):
    return PeriodicTaskService.run(task)


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')