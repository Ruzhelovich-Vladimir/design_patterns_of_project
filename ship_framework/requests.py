
class Request:
    """
    Базовый класс запросов Request
    """

    @staticmethod
    def parse_input_data(data):
        """ Получение словаря из строки формата URL """
        if data:
            return {key: value
                    for key, value in [params.split('=')
                                       for params in data.split('&')]}
        else:
            return {}

    def get_request_params(self, environ):
        """Получение параметров запроса"""
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)
        return request_params


class GetRequests(Request):
    """ POST - запросы """
    pass


class PostRequests(Request):
    """ GET - запросы """

    @staticmethod
    def get_wsgi_input_data(env: dict) -> bytes:
        """ Получение параметров из подзапроса (в теле запроса) """

        # Получаем длину контекста в виде строки
        content_length_data = env.get('CONTENT_LENGTH')
        # Получаем длину контекста в виде числа
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные из контекста если они есть
        return env['wsgi.input'].read(content_length) \
            if content_length > 0 else b''

    def parser_wsgi_input_data(self, data: bytes) -> dict:
        """ Получение словаря из строки """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_data(self, environ):
        """ Получение данных из подзапроса """
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parser_wsgi_input_data(data)
        return data


if __name__ == '__main__':

    print(Request.parse_input_data('val1=23&val2=34'))
