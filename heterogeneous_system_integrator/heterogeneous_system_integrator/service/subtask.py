from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.step import TransferStepService, TransformStepService


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository

    @classmethod
    def run(cls, subtask: Subtask):
        data = []
        try:
            for step in subtask.download_steps:
                data += TransferStepService.download_data(step)
            
            data = TransformStepService.transform_data(data, subtask.transform_step)
            TransferStepService.upload_data(data, subtask.upload_step)
        
        except TypeError as ex:
            return f'Subtask {str(subtask)} result: Exit code 1 - {str(ex)}.'

        return f'Subtask {str(subtask)} result: Exit code 0'
        