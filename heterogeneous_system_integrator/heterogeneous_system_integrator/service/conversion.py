from heterogeneous_system_integrator.domain.base import OPERATIONS
from heterogeneous_system_integrator.repository.conversion import ConversionRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.domain.conversion import Conversion


class ConversionService(BaseService):
    REPOSITORY_CLASS = ConversionRepository

    @classmethod
    def convert_data(cls, data: list[dict], conversions: list[Conversion]):
        for conversion in conversions:
            field_name = conversion.field_name
            operator = conversion.comparison_operator
            comparision_value = conversion.comparison_value
            new_value = conversion.conversion_value

            for row in data:
                if not row.get(field_name):
                    raise TypeError(f'Field name from Conversion {str(conversion)} config is incorrect. There is no such field as {field_name} in the data.')
                
                if OPERATIONS[operator](row[field_name], comparision_value):
                    row[field_name] = new_value 

        return data
