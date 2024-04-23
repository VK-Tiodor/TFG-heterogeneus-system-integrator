from heterogeneous_system_integrator.repository.mapping import MappingRepository
from heterogeneous_system_integrator.domain.mapping import Mapping
from heterogeneous_system_integrator.service.base import BaseService


class MappingService(BaseService):
    REPOSITORY_CLASS = MappingRepository

    @classmethod
    def map_data(cls, data: list[dict], mappings: list[Mapping], discard_leftover_fields: bool):
        new_data = []
        
        for row in data:
            old_row = row.copy()
            new_row = {}

            for mapping in mappings:
                origin_field_name = mapping.origin_field_name
                origin_constant_value = mapping.constant_value
                destination_field_name = mapping.destination_field_name

                if origin_field_name and not row.get(origin_field_name):
                    raise TypeError(f'Field name from Mapping {str(mapping)} config is incorrect. There is no such field as {origin_field_name} in the data.')
                
                new_row[destination_field_name] = old_row.pop(origin_field_name) if origin_field_name else origin_constant_value

            if not discard_leftover_fields:
                new_row.update(old_row)

            new_data += [new_row]

        return new_data