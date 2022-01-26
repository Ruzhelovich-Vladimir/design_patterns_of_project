"""
Поведенческий паттерн - Шаблонный метод
"""
from ship_framework.templator import render

class TemplateView:
    """ Шаблон контроллера
    Данный шаблон используется с реализации контроллеров,
    при необходимости необходимо переопределить методы и свойства.
    """

    template_name = 'template.html'
    template_path = 'templates'

    @staticmethod
    def get_context_data():
        """ Получение данных контекста """
        return {}

    def get_template(self):
        """ Получение имени шаблона HTML-файла """
        return self.template_name

    def render_template_with_context(self, template_name: str):
        """ Вернуть страницу """
        context = self.get_context_data()
        return '200 OK', [render(template_name,
                                 self.template_path, **context).encode()]

    def render_template_without_context(self, template_name: str):
        """ Вернуть страницу """
        context = self.get_context_data()
        return '200 OK', [render(template_name,
                                 self.template_path, **context).encode()]

    def __call__(self, request):
        """ Обработчик """
        return self.render_template_with_context(self.template_name)


class ListView(TemplateView):
    """ Шаблон контроллера списка """

    queryset = []
    """ Список данных """
    template_name = 'list_template.html'
    """ HTML - шаблон """
    context_object_name = 'objects_list'
    """ наименование объекта списка для передачи в шаблон """

    def get_queryset(self):
        """ Получить данные queryset """
        return self.queryset

    def get_context_object_name(self):
        """ Получить наименование объекта для передачи в контекст """
        return self.context_object_name

    def get_context_data(self):
        """ Получение объекта для передачи в контекст """
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    """ Шаблон контроллера создания """
    template_name = 'create_template.html'
    redirect_template_name = None

    @staticmethod
    def get_request_data(request):
        """ Получение данных их запроса """
        return request['data']

    def create_object(self, data):
        """ Функция создания объекта """
        pass

    def __call__(self, request):
        """ Обработчик """
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            if self.redirect_template_name:
                pass
                # TODO реализовать редирект
            return self.render_template_with_context(self.template_name)
        # Иначе вызываем форму создания
        return super().__call__(request)
