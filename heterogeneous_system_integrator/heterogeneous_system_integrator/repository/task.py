from datetime import datetime, timedelta

from django.db import IntegrityError 
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask, PeriodicTask
from heterogeneous_system_integrator.heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.repository.base import BaseRepository
from heterogeneous_system_integrator.settings import CELERY_PLANNED_TASK_NAME, CELERY_PERIODIC_TASK_NAME


class AsyncTaskRepository(BaseRepository):
    MODEL_CLASS = AsyncTask


class PlannedTaskRepository(BaseRepository):
    MODEL_CLASS = PlannedTask

    @classmethod
    def _validate_fields(cls, model: PlannedTask):
        if (datetime(model.execute_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Execute at" must be fulfilled with a date in the future')

    @classmethod
    def _pre_save_model_operations(cls, model: Base):
        clock = ClockedSchedule(clocked_time=model.execute_at)
        clock.save()
        properties = dict(name=model.name, task=CELERY_PLANNED_TASK_NAME, clocked=clock, kwargs={"task": model})
        planned_task = PeriodicTask.objects.update_or_create(defaults=properties, name=model.name)[0]
        model.celery_task = planned_task
        return super()._pre_save_model_operations(model)
    
    # TODO BULK pre_save

class PeriodicTaskRepository(BaseRepository):
    MODEL_CLASS = PeriodicTask

    @classmethod
    def _validate_fields(cls, model: PeriodicTask):
        if model.stop_at and (datetime(model.stop_at) - datetime.now()) <= timedelta(0):
            raise IntegrityError('"Stop at" must be fulfilled with a date from the future')

    @classmethod
    def _pre_save_model_operations(cls, model: Base):
        properties = dict(name=model.name, task=CELERY_PERIODIC_TASK_NAME, crontab=model.period.celery_crontab, kwargs={"task": model}, expires=model.stop_at)
        periodic_task = PeriodicTask.objects.update_or_create(defaults=properties, name=model.name)[0]
        model.celery_task = periodic_task
        return super()._pre_save_model_operations(model)
    
    # TODO BULK pre_save
