from heterogeneous_system_integrator.domain.base import OPERATIONS
from heterogeneous_system_integrator.domain.filter import Filter, FILTER_TYPE_KEEP
from heterogeneous_system_integrator.repository.filter import FilterRepository
from heterogeneous_system_integrator.service.base import BaseService


class FilterService(BaseService):
    REPOSITORY_CLASS = FilterRepository

    @classmethod
    def filter_data(cls, filter_: Filter, data: list[dict]) -> list[dict]:        
        filtered_data = []
        field_name = filter_.field_name
        operator = filter_.comparison_operator
        keep = (filter_.type == FILTER_TYPE_KEEP)
        
        for row in data:
            if not row.get():
                raise TypeError(f'Field name from Filter {str(field_name)} config is incorrect. There is no such field as {field_name} in the data.')
            
            if (OPERATIONS[operator](row[field_name]) and keep) or (not OPERATIONS[operator](row[field_name]) and not keep):
                filtered_data += [row]

        return filtered_data
            
