from heterogeneous_system_integrator.domain.base import OPERATIONS
from heterogeneous_system_integrator.domain.filter import Filter, FILTER_TYPE_KEEP
from heterogeneous_system_integrator.repository.filter import FilterRepository
from heterogeneous_system_integrator.service.base import BaseService


class FilterService(BaseService):
    REPOSITORY_CLASS = FilterRepository

    @classmethod
    def filter_data(cls, data: list[dict], filters: list[Filter]) -> list[dict]:        
        filtered_data = []
        for filter_ in filters:
            field_name = filter_.field_name
            operator = filter_.comparison_operator
            comparison_value = filter_.comparison_value
            keep = (filter_.type == FILTER_TYPE_KEEP)
            
            for row in data:
                if not row.get():
                    raise TypeError(f'Field name from Filter {str(filter_)} config is incorrect. There is no such field as {field_name} in the data.')
                
                if (OPERATIONS[operator](row[field_name], comparison_value) and keep) or (not OPERATIONS[operator](row[field_name], comparison_value) and not keep):
                    filtered_data += [row]

        return filtered_data
            
