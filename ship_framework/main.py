from quopri import decodestring
from wsgiref.simple_server import make_server
from .requests import GetRequests, PostRequests

class Application:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

        # Start httpd
        with make_server('', 8000, self) as httpd:
            url = f'http://127.0.0.1:8000/'

            print(f'Server is starting on port {url}...')
            httpd.serve_forever()

    def __call__(self, environ, start_response):

        path = environ["PATH_INFO"]
        if path in self.routes:
            view = self.routes[path]
        else:
            view = self.not_found_404_views

        request = {}
        self.add_request_info(request, self.fronts)  # Добавляет в запрос доп. информацию
        request['method'] = environ['REQUEST_METHOD']  # Добавляет в запрос метод

        if request['method'] == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = self.decode_value(data)  # Перекодирование словаря в utf-8
            print(f'Пришел POST-параметры: {data}')
        elif request['method'] == 'GET':
            data = GetRequests().get_request_params(environ)
            request['request_params'] = self.decode_value(data)  # Перекодирование словаря в utf-8
            print(f'Пришли GET-параметры: {data}')

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return body

    @staticmethod
    def not_found_404_views(request):
        #print(request)
        return '404 WHAT', [b'404 PAGE Not Found']

    @staticmethod
    def add_request_info(request, fronts=[]):
        for front in fronts:
            front(request)

    @staticmethod
    def decode_value(data):
        """ Перекодирование словаря в utf-8 """
        new_data = {}
        for k, v in data.items():
            val = bytes(replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

