from csv import DictWriter
from io import BufferedWriter
import os


class CsvWriter:

    def __init__(self, file_name, delete_on_exit: bool = False):
        self.file_path = os.path.join(os.path.dirname(__file__), 'temp_files', file_name)
        self.delete_on_exit = delete_on_exit
        self.written_file = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.written_file:
            self.written_file.close()

        if os.path.exists(self.file_path) and self.delete_on_exit:
            os.remove(self.file_path)

    @classmethod
    def _get_column_names_from_data(cls, data: list[dict]) -> set:
        column_names = set()
        for row in data:
            column_names = column_names.union(set(row.keys()))
        return column_names

    def write_file(self, data: list[dict]):
        with open(self.file_path, 'w') as file:
            writer = DictWriter(file, fieldnames=self._get_column_names_from_data(data))
            writer.writeheader()
            writer.writerows(data)

        self.written_file = open(self.file_path, 'rb')
        return self.written_file
