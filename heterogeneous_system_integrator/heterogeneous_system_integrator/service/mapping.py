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
            mappings_with_constants = list(filter(lambda x: bool(x.constant_value), mappings))
            mappings_with_fields = list(filter(lambda x: bool(x.origin_field_name), mappings))
            mappings_with_fields = sorted(mappings_with_fields, key=(lambda x: x.origin_field_name.count('.')))

            for mapping in mappings_with_fields:
                if not row.get(mapping.origin_field_name):
                    raise TypeError(f'Field name from Mapping {str(mapping)} config is incorrect. There is no such field as {mapping.origin_field_name} in the data.')
                
                origin_value = cls._get_value_from_row_field(old_row, mapping.origin_field_name)
                new_row = cls._set_value_in_row_field(origin_value, new_row, mapping.destination_field_name)
            
            for mapping in mappings_with_constants:
                new_row = cls._set_value_in_row_field(mapping.constant_value, new_row, mapping.destination_field_name)

            if not discard_leftover_fields:
                new_row.update(old_row)

            new_data += [new_row]

        return new_data
    
    @classmethod
    def _set_value_in_row_field(cls, value: str, row: dict, field_name: str) -> dict:
        field_names = field_name.split('.')
        inner_fields = aux = {}
        
        for field in field_names[:-1]:
            aux[field] = {}
            aux = aux[field]
 
        aux[field_names[-1]] = value
        row.update(inner_fields)
        return row
    
    @classmethod
    def _get_value_from_row_field(cls, row: dict, field_name: str) -> dict:
        field_names = field_name.split('.')
        origin_field = row
        
        for field in field_names[:-1]:
            origin_field = row[field]

        value = origin_field.pop(field_names[-1])
        return value