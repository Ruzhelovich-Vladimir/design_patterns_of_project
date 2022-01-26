"""
Поведенческий паттерн - "Наблюдатель"
"""
from abc import ABCMeta, abstractmethod
from jsonpickle import dumps, loads


class Observer(metaclass=ABCMeta):
    """ Наблюдатель """
    @abstractmethod
    def update(self, subject):
        pass


class EmailNotifier(Observer):
    """ Уведомление по EMAIL"""

    def update(self, msg):
        print('EMAIL->', self, msg)


class SmsNotifier(Observer):
    """ Уведомление по SMS"""

    def update(self, msg):
        print('SMS->', self, msg)


class ObservationSubject:
    """ Субъект наблюдения """

    # Не очень понравилось определять методы нотификации в модуле views.py
    # Хотел бы сделать более универсально, чтобы работало в любом классе
    observers = [EmailNotifier, SmsNotifier]

    def notify(self, msg):
        """ Отправка уведомлений
        msg: (строка) - сообщение
        """
        for item in self.observers:
            item.update(self, msg)


class BaseSerializer:
    """ Класс серилизации, прототип функции REST API GET """

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)
