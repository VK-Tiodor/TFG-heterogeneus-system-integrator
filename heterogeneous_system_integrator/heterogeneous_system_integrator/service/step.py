from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep
from heterogeneous_system_integrator.repository.step import TransferStepRepository, TransformStepRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.conversion import ConversionService
from heterogeneous_system_integrator.service.data_location import ApiDataLocationService, DbDataLocationService, FtpDataLocationService
from heterogeneous_system_integrator.service.filter import FilterService
from heterogeneous_system_integrator.service.mapping import MappingService

class TransferStepService(BaseService):
    REPOSITORY_CLASS = TransferStepRepository

    @classmethod
    def download_data(cls, step: TransferStep) -> list[dict]:
        data_location = step.data_location
        
        if isinstance(data_location, ApiDataLocation):
            data = ApiDataLocationService.download_data(data_location)
        
        elif isinstance(data_location, DbDataLocation):
            data = DbDataLocationService.download_data(data_location)
        
        else:
            data = FtpDataLocationService.download_data(data_location)

        data = FilterService.filter_data(data, step.filters)
        
        return data

    @classmethod
    def upload_data(cls, data: list[dict], step: TransferStep) -> list[str]:
        data_location = step.data_location

        data = FilterService.filter_data(data, step.filters)

        if isinstance(data_location, ApiDataLocation):
            responses = ApiDataLocationService.upload_data(data_location, data)
        
        elif isinstance(data_location, DbDataLocation):
            responses = DbDataLocationService.upload_data(data_location, data)
        
        else:
            responses = FtpDataLocationService.upload_data(data_location, data)

        return responses


class TransformStepService(BaseService):
    REPOSITORY_CLASS = TransformStepRepository

    @classmethod
    def transform_data(cls, data: list[dict], step: TransformStep) -> None:
        mappings = step.mappings
        discard_leftover_fields = step.discard_leftover_fields
        conversions = step.conversions
        mappings_first = step.conversions_after_mappings
        
        if mappings_first:
            data = MappingService.map_data(data, mappings, discard_leftover_fields)
            data = ConversionService.convert_data(data, conversions)
        
        else:
            data = ConversionService.convert_data(data, conversions)
            data = MappingService.map_data(data, mappings, discard_leftover_fields)
        
        return data