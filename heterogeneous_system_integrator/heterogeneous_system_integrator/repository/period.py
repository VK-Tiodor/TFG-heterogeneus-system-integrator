from django.db import IntegrityError
from django.db.models import QuerySet
from django_celery_beat.models import CrontabSchedule

from heterogeneous_system_integrator.domain.period import Period
from heterogeneous_system_integrator.repository.base import BaseRepository
from heterogeneous_system_integrator.settings import TIME_ZONE


class PeriodRepository(BaseRepository):
    MODEL_CLASS = Period

    @classmethod
    def _validate_fields(cls, model: Period):
        if not any([model.minute, model.hour, model.day_of_week, model.day_of_month, model.month_of_year]):
            raise IntegrityError('At least one field must be fulfilled')
        
    @classmethod
    def _pre_save_model_operations(cls, model: Period):
        cls._validate_fields(model)
        crontab = CrontabSchedule(
            minute=model.minute,
            hour=model.hour,
            day_of_week=model.day_of_week,
            day_of_month=model.day_of_month,
            month_of_year=model.month_of_year,
            timezone=TIME_ZONE
        )
        crontab.save()
        model.celery_crontab = crontab
        super()._pre_save_model_operations(model)

    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[Period]):
        celery_crontabs = []
        for model in models:
            cls._validate_fields(model)
            crontab = CrontabSchedule(model.minute, model.hour, model.day_of_week, model.day_of_month, model.month_of_year)
            model.celery_crontab = crontab
            celery_crontabs += [crontab]
        CrontabSchedule.objects.bulk_create(celery_crontabs)
        super()._pre_save_multiple_models_operations(models)

    @classmethod
    def _post_delete_model_operations(cls, model: Period) -> None:
        super()._post_delete_model_operations(model)
        crontab = model.celery_crontab
        crontab.delete()
    
    @classmethod
    def _post_delete_query_operations(cls, query: QuerySet[Period]) -> None:
        super()._post_delete_query_operations(query)
        crontab_pks = []
        
        for model in query:
            crontab_pks += [model.celery_crontab]

        CrontabSchedule.objects.filter(pk__in=crontab_pks).delete()
