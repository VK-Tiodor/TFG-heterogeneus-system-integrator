from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation
from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep
from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.data_location import ApiDataLocationService, DbDataLocationService, FtpDataLocationService
from heterogeneous_system_integrator.service.filter import FilterService


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository

    @classmethod
    def run(cls, subtask: Subtask):
        data = []
        try:
            for step in subtask.download_steps:
                data += cls._download_data(step)
            
            cls._transform_data(data, subtask.transform_step)
            cls._upload_data(data, subtask.upload_step)
        
        except TypeError as ex:
            return f'Subtask {str(subtask)} result: Exit code 1 - {str(ex)}.'

        return f'Subtask {str(subtask)} result: Exit code 0'
        
    @classmethod
    def _download_data(cls, step: TransferStep) -> list[dict]:
        data_location = step.data_location
        filters = step.filters
        
        if isinstance(data_location, ApiDataLocation):
            data = ApiDataLocationService.download_data(data_location)
        elif isinstance(data_location, DbDataLocation):
            data = DbDataLocationService.download_data(data_location)
        else:
            data = FtpDataLocationService.download_data(data_location)
        
        for filter_ in filters:
            data = FilterService.filter_data(filter_, data)
        
        return data

    @classmethod
    def _transform_data(cls, data: list[dict], step: TransformStep) -> None:
        pass

    @classmethod
    def _upload_data(cls, data: list[dict], step: TransferStep) -> None:
        pass