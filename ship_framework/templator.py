from jinja2.environment import Environment
from jinja2 import FileSystemLoader

def render(template_name, folder='templates', **kwargs):

    # Объект окружения
    env = Environment()
    # Каталог для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)

if __name__ == '__main__':

    goods = [{'name': f'Товар #{inx}', 'price': inx*100} for inx in range(1, 5)]
    print(render(path='test.html', title='Test title', goods=goods))

