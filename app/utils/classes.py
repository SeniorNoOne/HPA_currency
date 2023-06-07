import csv
import os.path
import sqlite3


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


class SQLiteWriter:
    def __init__(self, db_name, table_queries, insert_query):
        self.db_name = db_name
        self.table_queries = table_queries
        self.insert_query = insert_query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

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

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def write_row(self, data):
        self.execute_query(self.insert_query,
                           (data['car_id'],
                            data['data_link'],
                            data['mileage'],
                            data['car_decs'],
                            data['engine'])
                           )
