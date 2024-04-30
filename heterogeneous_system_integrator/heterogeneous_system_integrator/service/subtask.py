from itertools import zip_longest

from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.step import TransferStepService, TransformStepService


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository

    @classmethod
    def run(cls, subtask: Subtask):
        data_lists = []
        try:
            for step in subtask.download_steps.all():
                data_lists += TransferStepService.download_data(step)

            data = cls._merge_data(subtask.merge_field_name, data_lists)
            data = TransformStepService.transform_data(data, subtask.transform_step)
            responses = TransferStepService.upload_data(data, subtask.upload_step)
        
        except Exception as ex:
            return f'Exit code 1 - {str(ex)}.'
        
        result_msg = ''
        for i, response in enumerate(responses):
            msg_separator = '*' * 32 + ' ' * 4 + f'BATCH {i} RESULTS' + ' ' * 4 + '*' * 32
            result_msg = f'{result_msg}{msg_separator}\n{response}\n'
        
        return result_msg
    
    @classmethod
    def _merge_data(cls, merge_field_name: str, data_lists: list[list[dict]]):
        data_lists = cls._sort_data_lists_for_quick_merge(merge_field_name, data_lists)
        merged_data = data_lists.pop()
        
        for data in data_lists:
            merged_data = cls._quick_merge(merged_data, data)
        
        return merged_data

    @classmethod
    def _sort_data_lists_for_quick_merge(cls, merge_field_name: str, data_lists: list[list[dict]]):
        data_lists = sorted(data_lists, key=lambda x: len(x))
        try:
            data_lists = [sorted(data, lambda x: x[merge_field_name]) for data in data_lists]
        
        except KeyError as ex:
            raise TypeError(f'Merge field name from subtask config is incorrect. There is no such field as {merge_field_name} in the data.')
        
        return data_lists
    
    @classmethod
    def _quick_merge(cls, first_data_list: list[dict], second_data_list: list[dict], merge_field_name: str):
        i = j = 0
        while i < len(first_data_list) and j < len(second_data_list):
            if first_data_list[i][merge_field_name] > second_data_list[j][merge_field_name]:
                first_data_list = first_data_list[:i] + [second_data_list[j]] + first_data_list[i:]
                i += 1
                j += 1
            
            elif first_data_list[i][merge_field_name] < second_data_list[j][merge_field_name]:
                i += 1
            
            else:
                first_data_list[i].update(second_data_list[j])
        
        first_data_list = first_data_list + second_data_list[j:]
        return first_data_list
