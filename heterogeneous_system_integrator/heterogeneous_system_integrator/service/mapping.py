from heterogeneous_system_integrator.domain.mapping import Mapping
from heterogeneous_system_integrator.repository.mapping import MappingRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.utils.read import ObjectReader
from heterogeneous_system_integrator.utils.write import ObjectWriter


class MappingService(BaseService):
    REPOSITORY_CLASS = MappingRepository

    @classmethod
    def map_data(cls, data: list[dict], mappings: list[Mapping], keep_leftover_fields: bool):
        new_data = []
        
        for row in data:
            old_row = row.copy()
            new_row = {}
            mappings_with_constants = list(filter(lambda x: bool(x.constant_value), mappings))
            mappings_with_fields = list(filter(lambda x: bool(x.origin_field_name), mappings))
            mappings_with_fields = sorted(mappings_with_fields, key=(lambda x: x.origin_field_name.count('.')))

            for mapping in mappings_with_fields:
                if not row.get(mapping.origin_field_name.split('.')[0]):
                    raise TypeError(f'Field name from Mapping {str(mapping)} config is incorrect. There is no such field as {mapping.origin_field_name} in the data.')
                
                origin_value = ObjectReader.pop_field(old_row, mapping.origin_field_name)
                new_row = ObjectWriter.set_field(origin_value, new_row, mapping.destination_field_name)
            
            for mapping in mappings_with_constants:
                new_row = ObjectWriter.set_field(mapping.constant_value, new_row, mapping.destination_field_name)

            if keep_leftover_fields:
                new_row.update(old_row)

            new_data += [new_row]

        return new_data
