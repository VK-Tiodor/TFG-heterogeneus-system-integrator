from json import loads, dumps
from time import time

from celery import states

from heterogeneous_system_integrator.domain.base import OPERATIONS
from heterogeneous_system_integrator.domain.filter import Filter, FILTER_TYPE_KEEP
from heterogeneous_system_integrator.repository.filter import FilterRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.utils.read import ObjectReader


class FilterService(BaseService):
    REPOSITORY_CLASS = FilterRepository

    @classmethod
    def filter_data(cls, data: list[dict], filters: list[Filter]) -> tuple[list[dict], dict]:
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        if not filters:
            return data, exec_data

        init_time = time()
        filtered_data = []
        for row in data:
            for filter_ in filters:
                field_name = filter_.field_name
                operator = filter_.comparison_operator
                comparison_value = loads(filter_.comparison_value)
                keep = (filter_.type == FILTER_TYPE_KEEP)
                if not row.get(field_name.split('.')[0]):
                    exec_data['errors'] += 1
                    exec_time = round((time() - init_time) * 1000, 2)
                    exec_data['logs'] += [
                        f'{exec_time}ms > Field name from Filter "{str(filter_)}" config is incorrect. '
                        f'There is no such field as "{field_name}" in: {dumps(row)}'
                    ]

                field_value = ObjectReader.get_field(row, field_name)
                if (((OPERATIONS[operator](field_value, comparison_value) and keep)
                        or (not OPERATIONS[operator](field_value, comparison_value) and not keep))
                        and row not in filtered_data):
                    filtered_data += [row]

        exec_data['status'] = states.SUCCESS if not exec_data['errors'] else states.FAILURE
        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return filtered_data, exec_data
            
