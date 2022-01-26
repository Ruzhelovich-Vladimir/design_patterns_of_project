from patterns.behavioral_patterns.observer import BaseSerializer
from patterns.behavioral_patterns.template import ListView, CreateView
from patterns.creational_patterns.logger import Logger

from patterns.structural_patterns.decorates import AppRoute, Debug
from patterns.creational_patterns.engine import Engine
from ship_framework.templator import render

templates_path = 'app/templates'

site = Engine()
routes = {}
logger = Logger('main')


@AppRoute(routes, ['/', '/index'])
class ViewIndex:
    @Debug('Index')
    def __call__(self, request):
        logger.log('Индексная страница')
        return '200 OK', [render('index.html', templates_path).encode()]


@AppRoute(routes, ['/work'])
class ViewWork:
    @Debug('Work')
    def __call__(self, request):
        return '200 OK', [render('work.html', templates_path).encode()]


@AppRoute(routes, ['/about'])
class ViewAbout:
    @Debug('About')
    def __call__(self, request):
        return '200 OK', [render('about.html', templates_path).encode()]


@AppRoute(routes, ['/contact'])
class ViewContact:

    @Debug('Contact')
    def __call__(self, request):
        return '200 OK', [render('contact.html', templates_path).encode()]


@AppRoute(routes, ['/categories'])
class ViewCategoryList(ListView):
    """
    Контроллер списка категорий
    """
    queryset = site.categories
    template_name = 'categories.html'
    template_path = templates_path

    def __init__(self):
        logger.log('Список категорий')

# class ViewCategoryList:
#     """
#     Контроллер списка категорий
#     """
#
#     def __init__(self):
#         logger.log('Индексная страница')
#
#     @Debug('CategoryList')
#     def __call__(self, request):
#         return '200 OK', [render('categories.html', templates_path,
#                                  categories_list=site.categories).encode()]


@AppRoute(routes, ['/category_create'])
class ViewCategoryCreate(CreateView):
    """
    Контроллера создания категорий (оставил почти без изменения)
    """
    template_name = 'category_create.html'
    redirect_template_name = '/categories'
    template_path = templates_path

    def create_object(self, data: dict):

        # Наименование категории
        name = data['name']
        name = site.decode_value(name)

        # Поиск родительской категории
        category_id = int(data.get('parent_category_id'))
        category = site.find_category_by_id(category_id) \
            if category_id > -1 else None

        # Создаём новую категорию
        new_category = site.create_category(name, category)
        site.categories.append(new_category)

# class ViewCategoryCreate:
#     """
#     Контроллера создания категорий (оставил почти без изменения)
#     """
#
#     def __init__(self):
#         logger.log('Создание категории')
#
#     @Debug('CategoryCreate')
#     def __call__(self, request):
#         if request['method'] == 'POST':
#             # Получение данных
#             data = request['data']
#             name = data['name']
#             name = site.decode_value(name)
#
#             # Поиск родительской категории
#             category_id = int(data.get('parent_category_id'))
#             category = site.find_category_by_id(category_id) \
#                 if category_id > -1 else None
#
#             # Создаём новую категорию
#             new_category = site.create_category(name, category)
#             site.categories.append(new_category)
#
#             # Отправляем пользователя на страницу со списком категорий
#             return '200 OK', [render('categories.html', templates_path,
#                                      categories_list=site.categories).encode()]
#         else:
#             # Если запрос GET, то отправляем на страницу с формой пост запроса
#             return '200 OK', [render('category_create.html', templates_path,
#                                      categories_list=site.categories).encode()]


@AppRoute(routes, ['/products'])
class ViewProductList:
    """
    Контроллер списка продуктов
    """

    def __init__(self):
        logger.log('Список продуктов')

    def __call__(self, request):
        return '200 OK', [render('products.html', templates_path,
                                 products_list=site.products).encode()]


@AppRoute(routes, ['/api'])
class ViewProductListApi:
    """
    Прототип Get-запроса
    """
    def __init__(self):
        logger.log('Get запрос списка продуктов')

    @Debug('products_api')
    def __call__(self, request):
        return '200 OK', [BaseSerializer(site.products).save().encode()]


@AppRoute(routes, ['/product_create'])
class ViewProductCreate:
    """
    Контроллера создания продукта (оставил почти без изменения)
    """
    def __init__(self):
        logger.log('Создание продукта')

    @Debug('ProductCreate')
    def __call__(self, request):
        if request['method'] == 'POST':
            # Получение данных
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            # TODO Хорошая идея: создаю продукт, опираясь на принятые данные
            date = request['data']
            date['category'] = site.find_category_by_id(
                int(date['category_id']))
            product_type = request['request_params']['type']
            new_product = site.create_product(product_type, **data)
            site.products.append(new_product)

            # Отправляем пользователя на страницу со списком категорий
            return '200 OK', [render('products.html', templates_path,
                                     products_list=site.products).encode()]
        else:
            # Если запрос GET, то отправляем на страницу с формой пост запроса
            print(site.products)
            if 'request_params' in request \
                    and 'type' in request['request_params']:
                if request['request_params']['type'] == 'good':
                    template_name = 'good_create.html'
                else:
                    template_name = 'service_create.html'
                return '200 OK', [
                    render(template_name,
                           templates_path,
                           categories_list=site.categories).encode()]


@AppRoute(routes, ['/product_copy'])
class ViewProductCopy:
    """ Контроллер копирования продукта """
    def __init__(self):
        logger.log('Копирование продукта')

    @Debug('ProductCopy')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            product_id = int(request_params['id'])
            product = site.get_product_from_id(product_id)
            if product:
                new_name = f'{product.name}_copy'
                new_product = product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', [render('products.html', templates_path,
                                     products_list=site.products).encode()]

        except KeyError as err:
            print(err)
