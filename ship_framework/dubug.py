from ship_framework.main import Application


class DebugApplication(Application):
    """ WSGI - приложение для вывода отладочной информации """

    def __init__(self, routes_obj, fronts_obj):
        """ Инициализация объекта """

        # Получение объекта Application, которое расширяем функционал данного
        # класса
        self.application = Application(routes_obj, fronts_obj)
        # Т.к. DebugApplication был как дочерним классом, то мы вызываем
        # Инициализирующий метод родителя.
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        """ Обработчик """
        print('DEBUG:', env)
        return self.application(env, start_response)
