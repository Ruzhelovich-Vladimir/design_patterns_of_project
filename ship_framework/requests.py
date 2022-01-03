
# Решил общую функцию сделать вне классов
def parse_input_data(data):
    """ getting dict from string of POST request"""
    if data:
        return {key: value for key, value in [params.split('=') for params in data.split('&')]}
    else:
        return {}


class GetRequests:
    """ Working with GET requests """
    def __init__(self):
        """ Заглушка для PEP8"""
        pass

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:
    """ Working with POST requests """
    def __init__(self):
        """ Заглушка для PEP8"""
        pass

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """ Получение параметров из подзапроса (в теле запроса) """

        # Получаем длину контекста в виде строки
        content_length_data = env.get('CONTENT_LENGTH')
        # Получаем длину контекста в виде числа
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные из контекста если они есть
        return env['wsgi.input'].read(content_length) if content_length > 0 else b''

    @staticmethod
    def parser_wsgi_input_data(data: bytes) -> dict:
        """ Получение словаря из строки """

        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = parse_input_data(data_str)
        return result
    
    def get_request_params(self, environ):
        """ Получение параметров из подзапроса """
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parser_wsgi_input_data(data)
        return data

if __name__ == '__main__':
    print(parse_input_data('val1=23&val2=34'))