from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def create_table(self, sql: str):
        pass

    @abstractmethod
    def insert_data(self, sql: str, data: list):
        pass

    @abstractmethod
    def select_data(self, sql: str):
        pass

    @abstractmethod
    def add_column(self, alter_sql: str):
        pass
