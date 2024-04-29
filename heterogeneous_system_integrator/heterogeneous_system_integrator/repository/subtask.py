from django.db import IntegrityError
from django.db.models import QuerySet

from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.domain.base import Base
from heterogeneous_system_integrator.repository.base import BaseRepository


class SubtaskRepository(BaseRepository):
    MODEL_CLASS = Subtask

    @classmethod
    def _validate_fields(cls, model: Subtask):
        len_download_steps = model.download_steps.count()
        if len_download_steps < 1 or (len_download_steps > 1 and not model.merge_field_name):
            cls.delete_model(model)
            if len_download_steps < 1:
                raise IntegrityError(f'"Download steps" must be fulfilled with at least one step.')
            else:
                raise IntegrityError(f'"Merge field name" must be fulfilled with a unique identifier when there is more than one download step.')

    @classmethod
    def _post_save_model_operations(cls, model: Base) -> None:
        super()._post_save_model_operations(model)
        cls._validate_fields(model)
    
    #TODO
    @classmethod
    def _post_save_multiple_models_operations(cls, query: QuerySet) -> None:
        return super()._post_save_multiple_models_operations(query)