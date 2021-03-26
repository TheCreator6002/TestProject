import sqlite3
from sqlite3 import Error
from connection_database.conntection_database import DatabaseConnection


class SQLite3Connection(DatabaseConnection):
    def __init__(self, database_name: str):
        self.__database_name = database_name
        self.__connection = None

    def create_database(self):
        try:

            self.__connection = sqlite3.connect(f'{self.__database_name}.db')

        except Error:

            print(Error)

    def create_table(self, sql: str):
        cursor_obj = self.__connection.cursor()

        cursor_obj.executescript(sql)

        self.__connection.commit()

    def insert_data(self, sql: str, data: list):
        cursor_obj = self.__connection.cursor()
        cursor_obj.execute(sql, data)

        self.__connection.commit()

    def select_data(self, select_sql: str):
        cursor_obj = self.__connection.cursor()
        cursor_obj.execute(select_sql)

        data = cursor_obj.fetchall()

        return data

    def add_column(self, alter_sql: str):
        cursor_obj = self.__connection.cursor()
        cursor_obj.execute(alter_sql)

        self.__connection.commit()
