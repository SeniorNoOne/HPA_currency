import csv
import os
import sqlite3
import sys
from pathlib import Path


class CSVWriter:
    def __init__(self, file_dir: str, headers: list):
        path = Path(file_dir)
        if file_dir.endswith('.csv'):
            os.makedirs(path.parent, exist_ok=True)

        self.mode = 'a' if os.path.exists(file_dir) else 'w'
        self.csv_file_dir = file_dir
        self.csv_headers = headers
        self.write_file = open(self.csv_file_dir, self.mode, newline="", encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.write_file, fieldnames=self.csv_headers)

        if self.mode == 'w':
            self.csv_writer.writeheader()

    def __del__(self):
        self.close()

    def close(self):
        self.write_file.close()

    def write_row(self, row: dict):
        self.csv_writer.writerow(row)

    def write_rows(self, rows: list):
        self.csv_writer.writerows(rows)


class SQLiteWriter:
    def __init__(self, db_name, table_queries, insert_query):
        self.db_name = db_name
        self.table_queries = table_queries
        self.insert_query = insert_query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()
        self.is_conn_closed = False

    def __del__(self):
        self.close()

    def close(self):
        if not self.is_conn_closed:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        self.is_conn_closed = True

    def create_tables(self):
        if self.cursor is None:
            raise Exception("Please connect to the database first.")

        for table_query in self.table_queries:
            self.cursor.execute(table_query)

        self.connection.commit()

    def execute_query(self, query, params=None):
        if self.cursor is None:
            raise Exception("Please connect to the database first.")

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        self.connection.commit()

    def write_row(self, data):
        self.execute_query(self.insert_query,
                           (data['car_id'],
                            data['data_link'],
                            data['mileage'],
                            data['car_decs'],
                            data['engine'])
                           )


class SelfEvalFilePath:
    """
    Say there is a dir 'files' and in main.py some files are created in this dir
    Launching python scripts/main.py and cd scripts && python main.py will
    create files in different dirs

    This class helps to avoid such behaviour. Works only with dirs that are
    subdirs of project's root dir
    """
    def __init__(self, filepath: str = ""):
        self._filepath = filepath

    @property
    def filepath(self):
        current_path = os.getcwd().split(os.sep)
        new_path = []

        for item in current_path:
            if item in self._filepath:
                break
            new_path.append(item)
        else:
            return f"{os.sep}".join(current_path) + os.sep + self._filepath
        return f"{os.sep}".join(new_path) + os.sep + self._filepath


class ProgressBar:
    def __init__(self, decimals=1, length=30):
        # Max number or decimal_places before dot including it - 100.
        self._decimal_places = 4
        self.fill = '▣'
        self.empty = '▢'
        self.decimals = decimals
        self.length = length

    def show(self, iteration, total, msg=''):
        percent = f'{iteration / total * 100:.{self.decimals}f}%'
        percent = f'{percent:<{self.decimals + self._decimal_places}}'
        filled_length = int(self.length * iteration // total)
        bar = self.fill * filled_length + self.empty * (self.length - filled_length)
        full_bar = f'\r{percent} {bar} {msg}'
        sys.stdout.write(full_bar)

        if iteration == total:
            sys.stdout.write('\n')
