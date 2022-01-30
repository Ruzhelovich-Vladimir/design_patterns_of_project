"""
 Архитектурный системный паттерн - Data Mapper

 Цель данного модуля выполнения операций CRUD над базами данных sqlite
"""
import sqlite3
from abc import abstractmethod
from sqlite3 import connect

from patterns.creational_patterns.models import Category, Product


class Mapper:
    """ Класс общих методов """
    tablename = None

    def __init__(self, connection):

        if not self.tablename or not isinstance(self.tablename, str):
            raise ValueError('Не задана имя таблицы')
        self.connection = connection
        self.cursor = connection.cursor()

    def all(self):
        """ Получение данных из таблицы базы данных """
        return []

    @abstractmethod
    def find_by_id(self, id):
        """ Абстрактный метод получение объекта по id  """
        pass

    def insert(self, obj):
        """ Добавление объекта в таблицу базы данных """
        statement = f"INSERT INTO {self.tablename} (name, parent_category) " \
                    f"VALUES (?,?)"
        self.cursor.execute(statement, (obj.name, obj.parent_category.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        """ Обновление объекта в таблице базы данных """
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        """ Удаление объекта в таблице базы данных """
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

class CategoryMapper(Mapper):

    def __init__(self, connection):
        self.tablename = 'category'
        super().__init__(connection)

    def all(self):
        """ Получение данных из таблицы базы данных """
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, parent_category = item
            category = Category(name, self.find_by_id(parent_category) if parent_category else None)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        """ Получение объекта по id  """
        statement = f'SELECT * FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))

        try:
            result = self.cursor.fetchone()
        except Exception as err:
            print(err)

        if result:
            return Category(result[1], result[2])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class ProductMapper(Mapper):

    def __init__(self, connection):
        self.tablename = 'product'
        super().__init__(connection)

    def find_by_id(self, id):
        """ Получение объекта по id  """
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=? LIMIT 1'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Product(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class DbCommitException(Exception):
    """ Исключение Commit """
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    """ Исключение Update """
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    """ Исключение Delete """
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    """ Исключение Found """
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


connection = connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'category': CategoryMapper,
        'product': Product
    }

    @staticmethod
    def get_mapper(obj):
        """ Получение """
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        elif isinstance(obj, Product):
            return ProductMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
