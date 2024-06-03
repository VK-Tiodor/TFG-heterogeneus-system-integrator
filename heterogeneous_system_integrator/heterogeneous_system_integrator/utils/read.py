
class ObjectReader:

    @classmethod
    def _find_dict_with_field(cls, row: dict, field_names: list[str]) -> dict:
        destination_dict = row
        for field in field_names[:-1]:
            destination_dict = row[field]
        return destination_dict

    @classmethod
    def pop_field(cls, row: dict, field_name: str) -> str:
        field_names = field_name.split('.')
        destination_dict = cls._find_dict_with_field(row, field_names)
        value = destination_dict.pop(field_names[-1])
        return value

    @classmethod
    def get_field(cls, row: dict, field_name: str) -> str:
        field_names = field_name.split('.')
        destination_dict = cls._find_dict_with_field(row, field_names)
        value = destination_dict.get(field_names[-1])
        return value