"""
Модуль движка
"""
from quopri import decodestring
from patterns.creational_patterns.models import BPObjectFactory, ProductFactory, Category


class Engine:
    """
    Класс движка
    """

    def __init__(self):
        self.customers = []
        self.distributors = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_business_partner(object_type):
        """
        Создание бизнес-партнёра
        """
        return BPObjectFactory.create(object_type)

    @staticmethod
    def create_category(name, parent_category=None):
        """
        Создание категории товара
        """
        return Category(name, parent_category)

    def get_child_category_list(self, parent_category):
        """
        Получение списка дочерних категорий
        """
        return [category for category in self.categories
                if category.category == parent_category]

    def find_category_by_id(self, key_id):
        """
        Поиск категорий по идентификатору
        """
        for item in self.categories:
            if item.id == key_id:
                return item
        raise Exception(f'Не найдена требуемая категория id = {key_id}')

    @staticmethod
    def create_product(product_type, **kwargs):
        """
        Создание продукта - Услуга или Товар
        """
        return ProductFactory.create(product_type, **kwargs)

    @staticmethod
    def get_attr_list(product_type):
        """
        Создание продукта - Услуга или Товар
        """
        return ProductFactory.get_attr_list(product_type)

    def get_product(self, name):
        """
        Поиск категорий продукта по имени
        """
        for item in self.products:
            if item.name == name:
                return item
        return None

    def get_product_from_id(self, id_product):
        """
        Поиск категорий продукта по имени
        """
        for item in self.products:
            if item.id == id_product:
                return item
        return None

    @staticmethod
    def decode_value(string_val):
        """
        Преобразовать любую строку в формат utf-8
        """
        byte_string = bytes(string_val.replace('%', '=').replace("+", " "),
                            'UTF-8')
        result = decodestring(byte_string).decode('UTF-8')
        return result
