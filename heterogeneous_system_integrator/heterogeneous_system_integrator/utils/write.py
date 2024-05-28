from csv import DictWriter
import os


class CsvWriter:

    def __init__(self, file_name, delete_on_exit: bool = False):
        self.file_path = os.path.join(os.path.dirname(__file__), 'temp_files', file_name)
        self.delete_on_exit = delete_on_exit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.file_path) and self.delete_on_exit:
            os.remove(self.file_path)

    def write_file(self, data: list[dict]):
        with open(self.file_path, 'w') as file:
            #TODO refinar
            columns = list(data[0].keys())
            writer = DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
