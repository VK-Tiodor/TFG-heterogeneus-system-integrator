from django.db import IntegrityError

from heterogeneous_system_integrator.domain.mapping import Mapping
from heterogeneous_system_integrator.repository.base import BaseRepository


class MappingRepository(BaseRepository):
    MODEL_CLASS = Mapping

    @classmethod
    def _validate_fields(cls, model: Mapping):
        if model.origin_field_name and model.constant_value:
            raise IntegrityError(f'"Origin field name" and "Constant value" are mutually exclusive. Only one must be fulfilled.')
        if not model.origin_field_name and not model.constant_value:
            raise IntegrityError(f'"Origin field name" and "Constant value" must be fulfilled.')

    @classmethod
    def _pre_save_model_operations(cls, model: Mapping):
        cls._validate_fields(model.origin_field_name, model.constant_value)
        super()._pre_save_model_operations(model)

    @classmethod
    def _pre_save_multiple_models_operations(cls, models: list[Mapping], fields: list[str] = None):
        for model in models:
            cls._validate_fields(model.origin_field_name, model.constant_value)
        super()._pre_save_multiple_models_operations(models, fields)
