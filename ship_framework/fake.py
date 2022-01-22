from ship_framework.dubug import DebugApplication


class FakeApplication(DebugApplication):
    """ WSGI - приложение для вывода отладочной информации """

    def __init__(self, routes_obj, fronts_obj):
        """ Инициализация объекта """

        # Получение объекта Application, которое расширяем функционал данного
        # класса
        self.application = DebugApplication(routes_obj, fronts_obj)
        # Т.к. DebugApplication был как дочерним классом, то мы вызываем
        # Инициализирующий метод родителя.
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        """ Обработчик """
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'FakeApplication']