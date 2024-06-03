from django.db import IntegrityError
from django.db.models import QuerySet, DateTimeField
from django.utils.timezone import datetime, timedelta
from django_celery_beat.models import ClockedSchedule, PeriodicTask as CeleryPeriodicTask

from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask, PeriodicTask
from heterogeneous_system_integrator.repository.base import BaseRepository
from heterogeneous_system_integrator.settings import CELERY_PLANNED_TASK_NAME, CELERY_PERIODIC_TASK_NAME


class AsyncTaskRepository(BaseRepository):
    MODEL_CLASS = AsyncTask


class _BaseScheduledTaskRepository(BaseRepository):
    
    @classmethod
    def _get_datetime_from_field(cls, field: DateTimeField):
        return datetime.strptime(str(field), '%Y-%m-%d %H:%M:%S%z')

    @classmethod
    def _get_time_difference(cls, field: DateTimeField):
        datetime_from_field = cls._get_datetime_from_field(field)
        return  datetime_from_field - datetime.now(datetime_from_field.tzinfo)

    @classmethod
    def _validate_fields(cls, model: PlannedTask | PeriodicTask):
        raise NotImplementedError

    @classmethod
    def _get_scheduled_task_fields(cls, model: PlannedTask | PeriodicTask):
        raise NotImplementedError

    @classmethod
    def _attach_scheduled_task_to_model(cls, model: PlannedTask | PeriodicTask):
        fields = cls._get_scheduled_task_fields(model)
        
        if not model.pk:
            scheduled_task = CeleryPeriodicTask(**fields)
        
        else:
            scheduled_task = CeleryPeriodicTask.objects.get(name=cls.get({'pk': model.pk}).name)
            for field_name, field_value in fields.items():
                setattr(scheduled_task, field_name, field_value)
        
        scheduled_task.save()
        model.celery_task = scheduled_task

    @classmethod
    def _pre_save_model_operations(cls, model: PlannedTask | PeriodicTask):
        cls._validate_fields(model)
        cls._attach_scheduled_task_to_model(model)
        return super()._pre_save_model_operations(model)
    
    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[PlannedTask | PeriodicTask], fields: list[str] = None):
        for model in models:
            cls._validate_fields(model)
            cls._attach_scheduled_task_to_model(model)
        
        if fields:
            fields += ['celery_task']
        
        return super()._pre_save_multiple_models_operations(models, fields)
    
    @classmethod
    def _post_delete_model_operations(cls, model: PlannedTask | PeriodicTask) -> None:
        super()._post_delete_model_operations(model)
        scheduled_task = model.celery_task
        scheduled_task.delete()

    @classmethod 
    def _post_delete_query_operations(cls, query: QuerySet[PlannedTask | PeriodicTask]) -> None:
        super()._post_delete_query_operations(query)
        scheduled_task_pks = []
        
        for model in query:
            scheduled_task_pks += [model.celery_task.pk]
            
        PeriodicTask.objects.filter(pk__in=scheduled_task_pks).delete


class PlannedTaskRepository(_BaseScheduledTaskRepository):
    MODEL_CLASS = PlannedTask

    @classmethod
    def _validate_fields(cls, model: PlannedTask):
        if cls._get_time_difference(model.execute_at) <= timedelta(0):
            raise IntegrityError('"Execute at" must be fulfilled with a date in the future')

    @classmethod
    def _get_scheduled_task_fields(cls, model: PlannedTask):
        clock = ClockedSchedule.objects.get_or_create(clocked_time=cls._get_datetime_from_field(model.execute_at))[0]
        return dict(name=model.name, task=CELERY_PLANNED_TASK_NAME, clocked=clock, kwargs={"task": model}, one_off=True)


class PeriodicTaskRepository(_BaseScheduledTaskRepository):
    MODEL_CLASS = PeriodicTask

    @classmethod
    def _validate_fields(cls, model: PeriodicTask):
        if model.stop_at and cls._get_time_difference(model.stop_at) <= timedelta(0):
            raise IntegrityError('"Stop at" must be fulfilled with a date from the future')

    @classmethod
    def _get_scheduled_task_fields(cls, model: PeriodicTask):
        return dict(
            name=model.name,
            task=CELERY_PERIODIC_TASK_NAME,
            crontab=model.period.celery_crontab,
            kwargs={"task": model},
            expires=cls._get_datetime_from_field(model.stop_at)
        )
