from time import time
from json import dumps

from celery import states

from heterogeneous_system_integrator.domain.mapping import Mapping
from heterogeneous_system_integrator.repository.mapping import MappingRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.utils.read import ObjectReader
from heterogeneous_system_integrator.utils.write import ObjectWriter


class MappingService(BaseService):
    REPOSITORY_CLASS = MappingRepository

    @classmethod
    def map_data(cls, data: list[dict], mappings: list[Mapping], keep_leftover_fields: bool) -> tuple[list[dict], dict]:
        new_data = []
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        init_time = time()
        for row in data:
            old_row = row.copy()
            new_row = {}
            mappings_with_constants = list(filter(lambda x: bool(x.constant_value), mappings))
            mappings_with_fields = list(filter(lambda x: bool(x.origin_field_name), mappings))
            mappings_with_fields = sorted(mappings_with_fields, key=(lambda x: x.origin_field_name.count('.')))
            for mapping in mappings_with_fields:
                if not row.get(mapping.origin_field_name.split('.')[0]):
                    exec_data['errors'] += 1
                    exec_time = round((time() - init_time) * 1000, 2)
                    exec_data['logs'] += [
                        f'{exec_time}ms > Field name from Mapping "{str(mapping)}" config is incorrect. '
                        f'There is no such field as "{mapping.origin_field_name}" in: {dumps(row)}'
                    ]
                    continue
                
                origin_value = ObjectReader.pop_field(old_row, mapping.origin_field_name)
                new_row = ObjectWriter.set_field(origin_value, new_row, mapping.destination_field_name)

            for mapping in mappings_with_constants:
                new_row = ObjectWriter.set_field(mapping.constant_value, new_row, mapping.destination_field_name)

            if keep_leftover_fields:
                new_row.update(old_row)

            new_data += [new_row]

        exec_data['status'] = states.SUCCESS if not exec_data['errors'] else states.FAILURE
        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return new_data, exec_data
