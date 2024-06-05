from celery import states

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
    def download_data(cls, step: TransferStep) -> tuple[list[dict] | dict, dict]:
        data_location = step.data_location
        results = {'transfer_step': str(step), 'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        if ApiDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = ApiDataLocationService.get({'name': data_location.name})
            data, exec_data = ApiDataLocationService.download_data(data_location)
        elif DbDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = DbDataLocationService.get({'name': data_location.name})
            data, exec_data = DbDataLocationService.download_data(data_location)
        else:
            data_location = FtpDataLocationService.get({'name': data_location.name})
            data, exec_data = FtpDataLocationService.download_data(data_location)

        results.update(exec_data)
        data, exec_data = FilterService.filter_data(data, step.filters.all())
        results['errors'] += exec_data['errors']
        results['logs'] += exec_data['logs']
        results['status'] = states.SUCCESS if not results['errors'] else states.FAILURE
        results['duration'] += exec_data['duration']
        return data, results

    @classmethod
    def upload_data(cls, data: list[dict], step: TransferStep) -> dict:
        data_location = step.data_location
        results = {'transfer_step': str(step), 'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        data, exec_data = FilterService.filter_data(data, step.filters.all())
        results.update(exec_data)
        if ApiDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = ApiDataLocationService.get({'name': data_location.name})
            exec_data = ApiDataLocationService.upload_data(data_location, data)
        elif DbDataLocationService.create_query({'name': data_location.name}).exists():
            data_location = DbDataLocationService.get({'name': data_location.name})
            exec_data = DbDataLocationService.upload_data(data_location, data)
        else:
            data_location = FtpDataLocationService.get({'name': data_location.name})
            exec_data = FtpDataLocationService.upload_data(data_location, data)

        results['errors'] += exec_data['errors']
        results['logs'] += exec_data['logs']
        results['status'] = states.SUCCESS if not results['errors'] else states.FAILURE
        results['duration'] += exec_data['duration']
        return results


class TransformStepService(BaseService):
    REPOSITORY_CLASS = TransformStepRepository

    @classmethod
    def transform_data(cls, data: list[dict], step: TransformStep) -> tuple[list[dict], dict]:
        mappings = step.mappings.all()
        keep_leftover_fields = step.keep_leftover_fields
        conversions = step.conversions.all()
        mappings_first = step.conversions_after_mappings
        results = {'transform_step': str(step), 'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        if mappings_first:
            data, exec_data_mapping = MappingService.map_data(data, mappings, keep_leftover_fields)
            data, exec_data_conversion = ConversionService.convert_data(data, conversions)
            results['logs'] = exec_data_mapping['logs'] + exec_data_conversion['logs']
        else:
            data, exec_data_conversion = ConversionService.convert_data(data, conversions)
            data, exec_data_mapping = MappingService.map_data(data, mappings, keep_leftover_fields)
            results['logs'] = exec_data_conversion['logs'] + exec_data_mapping['logs']

        results['errors'] = exec_data_conversion['errors'] + exec_data_mapping['errors']
        results['status'] = states.SUCCESS if not results['errors'] else states.FAILURE
        results['duration'] += exec_data_conversion['duration'] + exec_data_mapping['duration']
        return data, results
