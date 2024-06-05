from json import dumps
from time import time

from celery import states

from heterogeneous_system_integrator.domain.base import OPERATIONS
from heterogeneous_system_integrator.domain.conversion import Conversion
from heterogeneous_system_integrator.repository.conversion import ConversionRepository
from heterogeneous_system_integrator.service.base import BaseService
from heterogeneous_system_integrator.utils.read import ObjectReader
from heterogeneous_system_integrator.utils.write import ObjectWriter


class ConversionService(BaseService):
    REPOSITORY_CLASS = ConversionRepository

    @classmethod
    def convert_data(cls, data: list[dict], conversions: list[Conversion]) -> tuple[list[dict], dict]:
        exec_data = {'status': '', 'duration': 0, 'errors': 0, 'logs': []}
        init_time = time()
        for row in data:
            for conversion in conversions:
                field_name = conversion.field_name
                operator = conversion.comparison_operator
                comparison_value = conversion.comparison_value
                new_value = conversion.conversion_value
                if not row.get(field_name.split('.')[0]):
                    exec_data['errors'] += 1
                    exec_time = round((time() - init_time) * 1000, 2)
                    exec_data['logs'] += [
                        f'{exec_time}ms > Field name from Conversion "{str(conversion)}" config is incorrect. '
                        f'There is no such field as "{field_name}" in: {dumps(row)}'
                    ]
                    continue

                field_value = ObjectReader.get_field(row, field_name)
                if OPERATIONS[operator](field_value, comparison_value):
                    ObjectWriter.set_field(new_value, row, field_name)

        exec_data['status'] = states.SUCCESS if not exec_data['errors'] else states.FAILURE
        exec_time = round((time() - init_time) * 1000, 2)
        exec_data['duration'] = exec_time
        return data, exec_data
