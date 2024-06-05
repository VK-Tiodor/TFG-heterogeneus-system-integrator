from time import time

from celery import states

from heterogeneous_system_integrator.domain.subtask import Subtask
from heterogeneous_system_integrator.repository.subtask import SubtaskRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.service.step import TransferStepService, TransformStepService


class SubtaskService(BaseService):
    REPOSITORY_CLASS = SubtaskRepository

    @classmethod
    def _update_exec_data(cls, subtask_exec_data, step_exec_data):
        subtask_exec_data['steps'] += [step_exec_data]
        subtask_exec_data['errors'] += step_exec_data['errors']
        subtask_exec_data['duration'] += step_exec_data['duration']
        subtask_exec_data['status'] = states.SUCCESS if not step_exec_data['errors'] else states.FAILURE

    @classmethod
    def run(cls, subtask: Subtask) -> dict:
        data_lists = []
        results = {'subtask': str(subtask), 'status': '', 'duration': 0, 'errors': 0, 'steps': []}
        for step in subtask.download_steps.all():
            data, exec_data = TransferStepService.download_data(step)
            data_lists += [data]
            cls._update_exec_data(results, exec_data)

        merge_field_name = subtask.merge_field_name
        if not merge_field_name:
            data = list(*data_lists)
        else:
            data, exec_data = cls._merge_data(merge_field_name, data_lists)
            cls._update_exec_data(results, exec_data)

        cls._update_exec_data(results, exec_data)
        data, exec_data = TransformStepService.transform_data(data, subtask.transform_step)
        cls._update_exec_data(results, exec_data)
        exec_data = TransferStepService.upload_data(data, subtask.upload_step)
        cls._update_exec_data(results, exec_data)
        return results
    
    @classmethod
    def _merge_data(cls, merge_field_name: str, data_lists: list[list[dict]]) -> tuple[list[dict], dict]:
        merged_data = []
        exec_data = {
            'merge_step': f'Merging {len(data_lists)} lists using "{merge_field_name}" field name',
            'status': '',
            'duration': 0,
            'errors': 0, 'logs': []
        }
        init_time = time()
        try:
            data_lists = cls._sort_data_lists_for_quick_merge(merge_field_name, data_lists)
            merged_data = data_lists.pop()

            for data in data_lists:
                merged_data = cls._quick_merge(merged_data, data, merge_field_name)

        except Exception as ex:
            exec_data['errors'] = 1
            exec_time = round((time() - init_time) * 1000, 2)
            exec_data['logs'] = [f'{exec_time}ms > {str(ex)}']
            exec_data['status'] = states.FAILURE
        else:
            exec_data['status'] = states.SUCCESS

        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return merged_data, exec_data

    @classmethod
    def _sort_data_lists_for_quick_merge(cls, merge_field_name: str, data_lists: list[list[dict]]):
        data_lists = sorted(data_lists, key=lambda x: len(x))
        try:
            data_lists = [sorted(data, key=lambda x: x[merge_field_name]) for data in data_lists]
        
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
