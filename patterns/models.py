"""
Модуль паттернов
"""

from copy import deepcopy


# ПАТТЕРН -АБСТРАКТНЫЙ КЛАССА
class BPObject:
    """
    Абстрактный объект бизнес партнёров
    inn: ИНН предприятия (число)
    name: Наименование (строка)
    """

    def __init__(self, inn, name):
        self.inn = inn
        self.name = name


class Customer(BPObject):
    """
    Класс заказчика
    inn: ИНН предприятия (число)
    name: Наименование (строка)
    address: Адрес доставки
    """

    def __init__(self, inn, name, address):
        super().__init__(inn, name)
        self.address = address


class Distributor(BPObject):
    """
    Класс дистрибьютора
    """
    pass


# ПОРОЖДАЮЩИЙ ПАТТЕРН - ФАБРИЧНОГО КЛАССА
class BPObjectFactory:
    """
    Класс фабрики для создания объектов продаж
    """

    types = {
        'customer': Customer,
        'distributor': Distributor
    }

    @classmethod
    def create(cls, object_type):
        return cls.types[object_type]


# ПОРОЖДАЮЩИЙ ПАТТЕРН -  ПРОТОТИП
class ProductPrototype:
    """
    Прототип продукта - товара/услуги
    """

    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype):
    """
    Класс продукта - товара/услуги
    """
    auto_id = 0

    def __init__(self, **kwargs):
        self.id = Product.auto_id
        Product.auto_id += 1
        if 'name' not in kwargs:
            raise Exception('Нет атрибута name')
        elif 'category' not in kwargs:
            raise Exception('Нет атрибута category')
        elif 'price' not in kwargs:
            raise Exception('Нет атрибута price')

        self.name = kwargs['name']
        self.category = kwargs['category']
        self.price = kwargs['price']
        self.category.products.append(self)

    def __str__(self):
        return f'{self.category.name}/{self.name} - {self.price}'


class Service(Product):
    """
    Класс сервиса
    """
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def __str__(self):
        return f'Услуга: {self.category.name}/{self.name} - {self.price}'


class Good(Product):
    """
    Класс товара
    """
    def __init__(self, **kwargs):
        if 'wight' not in kwargs:
            raise Exception('Нет атрибута wight')
        elif 'volume' not in kwargs:
            raise Exception('Нет атрибута volume')
        super().__init__(**kwargs)
        self.wight = kwargs['wight']
        self.volume = kwargs['volume']

    def __str__(self):
        return f'Товар: {self.category.name}/{self.name} вес:{self.wight}, ' \
               f'объём: {self.volume}л. - {self.price}'


# ПОРОЖДАЮЩИЙ ПАТТЕРН - ФАБРИЧНОГО КЛАССА
class ProductFactory:
    """
    Порождающий класс
    """
    types = {
        'service': Service,
        'good': Good
    }

    @classmethod
    def create(cls, product_type, **kwargs):
        """
        Порождающий метод фабричного класса
        """
        return cls.types[product_type](**kwargs)

    @classmethod
    def get_attr_list(cls, product_type):
        """
        Получение списка атрибутов объекта
        """
        return [attr for attr in dir(cls.types[product_type])
                if not attr.startswith('__')]


class Category:
    """
    Класс категории
    """
    auto_id = 0

    def __init__(self, name, parent_category):
        """
        Добавляет новую категорию
        """

        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.parent_category = parent_category
        self.products = []

    @property
    def parent_category_name(self):
        """ Наименование родительской категории """
        if self.parent_category:
            return self.parent_category.name
        else:
            return 'Главная категория'

    def __str__(self):
        if self.parent_category:
            return f'{self.parent_category.name}/{self.name}'
        else:
            return f'Главная категория/{self.name}'

    def products_count(self):
        """
        Количество продуктов в категории
        """
        result = len(self.products)
        if self.products:
            result += self.products.count()
        return result