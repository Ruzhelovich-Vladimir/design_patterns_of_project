from time import time


class AppRoute:
    """ Декоратор AppRoute добавляет в список маршрута ulr и его контроллер
        Входные параметры:
        routes: словарь маршрутов
        url: строка url
    """

    def __init__(self, routes: dict, urls: list):
        """ Инициализация декоратора """
        self.routes = routes
        self.urls = urls

    def __call__(self, cls):
        """ Обработчик декоратора """
        # Добавляем в словарь вызов класса, в котором используется декоратор
        for url in self.urls:
            self.routes[url] = cls()


class Debug:
    """ Декоратор AppRoute добавляет в список маршрута ulr и его контроллер
            Входные параметры:
            name: строка
    """

    def __init__(self, name: str):
        """ Инициализация декоратора """
        self.name = name

    def __call__(self, cls):
        """ Обработчик декоратора """

        def time_decor(method):
            """ Функция - обёртки для метода любого метода класса"""

            def timer_call(*args, **kwargs):
                """ Обработчик вызова метода"""
                start_time = time()
                result = method(*args, **kwargs)
                finish_time = time()
                delta = finish_time - start_time
                print(f'debug: running {self.name} - {delta:2.2f}ms')
                # Передаём результат
                return result

            # Возвращаем ссылку на функцию обработчика
            return timer_call

        return time_decor(cls)
