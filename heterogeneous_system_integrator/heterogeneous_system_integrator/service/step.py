from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep
from heterogeneous_system_integrator.repository.step import TransferStepRepository, TransformStepRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.conversion import ConversionService
from heterogeneous_system_integrator.service.data_location import ApiDataLocationService, DbDataLocationService, FtpDataLocationService
from heterogeneous_system_integrator.service.filter import FilterService
from heterogeneous_system_integrator.service.mapping import MappingService
from heterogeneous_system_integrator.utils.write import CsvWriter


class TransferStepService(BaseService):
    REPOSITORY_CLASS = TransferStepRepository

    @classmethod
    def download_data(cls, step: TransferStep) -> list[dict]:
        data_location = step.data_location
        
        if ApiDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = ApiDataLocationService.get({'name': data_location.name})
            data = ApiDataLocationService.download_data(data_location)
        
        elif DbDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = DbDataLocationService.get({'name': data_location.name})
            data = DbDataLocationService.download_data(data_location)
        
        else:
            data_location = FtpDataLocationService.get({'name': data_location.name})
            data = FtpDataLocationService.download_data(data_location)

        data = FilterService.filter_data(data, step.filters.all())
        
        return data

    @classmethod
    def upload_data(cls, data: list[dict], step: TransferStep) -> list[str]:
        data_location = step.data_location

        data = FilterService.filter_data(data, step.filters.all())

        if ApiDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = ApiDataLocationService.get({'name': data_location.name})
            responses = ApiDataLocationService.upload_data(data_location, data)
        
        elif DbDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = DbDataLocationService.get({'name': data_location.name})
            responses = DbDataLocationService.upload_data(data_location, data)
        
        else:
            data_location = FtpDataLocationService.get({'name': data_location.name})
            #TODO Write fichero
            responses = FtpDataLocationService.upload_data(data_location, data)

        return responses


class TransformStepService(BaseService):
    REPOSITORY_CLASS = TransformStepRepository

    # TODO Validate
    @classmethod
    def transform_data(cls, data: list[dict], step: TransformStep) -> list[dict]:
        mappings = step.mappings.all()
        keep_leftover_fields = step.keep_leftover_fields
        conversions = step.conversions.all()
        mappings_first = step.conversions_after_mappings
        
        if mappings_first:
            data = MappingService.map_data(data, mappings, keep_leftover_fields)
            data = ConversionService.convert_data(data, conversions)
        
        else:
            data = ConversionService.convert_data(data, conversions)
            data = MappingService.map_data(data, mappings, keep_leftover_fields)
        
        return data