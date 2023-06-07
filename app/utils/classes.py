import csv
import os.path


class CSVWriter:
    def __init__(self, file_dir: str, headers: list):
        mode = 'a' if os.path.exists(file_dir) else 'w'

        self.csv_file_dir = file_dir
        self.csv_headers = headers
        self.write_file = open(self.csv_file_dir, mode, newline="", encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.write_file, fieldnames=self.csv_headers)
        self.csv_writer.writeheader()

    def __del__(self):
        self.close()

    def write_row(self, row: dict):
        self.csv_writer.writerow(row)

    def write_rows(self, rows: list):
        self.csv_writer.writerows(rows)

    def close(self):
        self.write_file.close()
