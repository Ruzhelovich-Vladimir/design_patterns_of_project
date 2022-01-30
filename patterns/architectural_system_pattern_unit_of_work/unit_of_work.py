"""
 Архитектурный системный паттерн - UnitOfWork

 DomainObject содержит класс по управлению транзакциями:
        self.insert_objects()
        self.update_objects()
        self.delete_objects()
 Цель данного класса абстрагироваться от объектов базы данных, а хранить
 и управлять операциями по добавлению, обновлению, удалению записей.

"""
from threading import local


class UnitOfWork:
    """
    Паттерн Unit work
    """
    current = local()

    def __init__(self):
        self.insert_objects_list = []  # Список объектов для INSERT FROM
        self.update_objects_list = []  # Список объектов для UPDATA
        self.delete_objects_list = []  # Список объектов для DELETE

    def set_mapper_registry(self, MapperRegistry):
        """ Регистрация маппера """
        self.MapperRegistry = MapperRegistry

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        """ Добавляем свойство со значением текущего класса"""
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        """ Получаем свойство со значением текущего класса"""
        return cls.current.unit_of_work

    def register_insert(self, obj):
        """ Регистрация нового объект в списке для добавления
            в рамках текущей транзакции
        """
        self.insert_objects_list.append(obj)

    def register_update(self, obj):
        """ Регистрация объект в списке
            для обновления в рамках текущей транзакции
        """
        self.update_objects_list.append(obj)

    def register_delete(self, obj):
        """ Регистрация объект в списке
            для удаления в рамках текущей транзакции
        """
        self.update_objects_list.append(obj)

    def insert_objects(self):
        """
        Вставляем все объекты из списка
        """
        for obj in self.insert_objects_list:
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def update_objects(self):
        """
        Обновляем все объекты из списка
        """
        for obj in self.insert_objects_list:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def delete_objects(self):
        """
        Удаляем все объекты из списка
        """
        for obj in self.insert_objects_list:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    def commit(self):
        """
        Выполняем все операции транзакции
        """
        self.insert_objects()
        self.update_objects()
        self.delete_objects()
        # Очистка списка транзакций
        self.insert_objects_list.clear()
        self.update_objects_list.clear()
        self.delete_objects_list.clear()


class DomainObject:
    """ Демон объекта - предок для моделей"""
    def mark_insert(self):
        """ Добавляем объект в список для добавления """
        UnitOfWork.get_current().register_insert(self)

    def mark_update(self):
        """ Добавляем объект в список для обновления """
        UnitOfWork.get_current().register_update(self)

    def mark_delete(self):
        """ Добавляем объект в список для удаления """
        UnitOfWork.get_current().register_delete(self)

