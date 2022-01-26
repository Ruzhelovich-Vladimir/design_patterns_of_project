"""
Поведенческий паттерн - Стратегия
"""


class ConsoleWriter:
    """ Запись в консоль """

    @staticmethod
    def write(text):
        """ Метод записи """
        print(text)


class FileWriter:
    """ Запись в файл """
    def __init__(self):
        """ Инициализация """
        self.file_name = 'log'

    def write(self, text):
        """ Метод записи """
        with open(self.file_name, 'a', encoding='utf-8') as file_handler:
            file_handler.write(f'{text}\n')
