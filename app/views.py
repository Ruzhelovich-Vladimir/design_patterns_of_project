from patterns.decorates import AppRoute, Debug
from patterns.engine import Engine
from ship_framework.templator import render

templates_path = 'app/templates'

site = Engine()
routes = {}


@AppRoute(routes, ['/', '/index'])
class ViewIndex:
    @Debug('Index')
    def __call__(self, request):
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


@AppRoute(routes, ['/Blog'])
class ViewBlog:

    @Debug('Blog')
    def __call__(self, request):
        blogs = [
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
              <b>Spider-Man</b> is a fictional character, a comic book
              superhero that appears in comic books published by Marvel
              Comics. Created by writer-editor Stan Lee and writer-artist
              Steve Ditko, he first appeared in Amazing Fantasy #15
              (cover-dated Aug. 1962).

              Lee and Ditko conceived the character as an orphan being raised
              by his Aunt May and Uncle Ben, and as a teenager, having to deal
              with the normal struggles of adolescence in addition to those of
              a costumed crimefighter.
              """
            },
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
                      <b>Spider-Man</b> is a fictional character, a comic book
                      superhero that appears in comic books published by
                      Marvel Comics. Created by writer-editor Stan Lee and
                      writer-artist Steve Ditko, he first appeared in Amazing
                      Fantasy #15 (cover-dated Aug. 1962).
                      Lee and Ditko conceived the character as an orphan being
                      raised by his Aunt May and Uncle Ben, and as a teenager,
                      having to deal with the normal struggles of adolescence
                      in addition to those of a costumed crimefighter.
                      """
            },
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
                      <b>Spider-Man</b> is a fictional character, a comic book
                      superhero that appears in comic books published by
                      Marvel Comics. Created by writer-editor Stan Lee and
                      writer-artist Steve Ditko, he first appeared in Amazing
                      Fantasy #15 (cover-dated Aug. 1962).
                      Lee and Ditko conceived the character as an orphan
                      being raised by his Aunt May and Uncle Ben, and as a
                      teenager, having to deal with the normal struggles of
                      adolescence in addition to those of a costumed
                      crimefighter.
                      """
            }
        ]

        return '200 OK', [render('blog.html', templates_path,
                                 blogs=blogs).encode()]


@AppRoute(routes, ['/contact'])
class ViewContact:

    @Debug('Contact')
    def __call__(self, request):
        return '200 OK', [render('contact.html', templates_path).encode()]


@AppRoute(routes, ['/categories'])
class ViewCategoryList:
    """
    Контроллер списка категорий
    """

    @Debug('CategoryList')
    def __call__(self, request):
        return '200 OK', [render('categories.html', templates_path,
                                 categories_list=site.categories).encode()]


@AppRoute(routes, ['/category_create'])
class ViewCategoryCreate:
    """
    Контроллера создания категорий (оставил почти без изменения)
    """

    @Debug('CategoryCreate')
    def __call__(self, request):
        if request['method'] == 'POST':
            # Получение данных
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            # Поиск родительской категории
            category_id = int(data.get('parent_category_id'))
            category = site.find_category_by_id(category_id) \
                if category_id > -1 else None

            # Создаём новую категорию
            new_category = site.create_category(name, category)
            site.categories.append(new_category)

            # Отправляем пользователя на страницу со списком категорий
            return '200 OK', [render('categories.html', templates_path,
                                     categories_list=site.categories).encode()]
        else:
            # Если запрос GET, то отправляем на страницу с формой пост запроса
            return '200 OK', [render('category_create.html', templates_path,
                                     categories_list=site.categories).encode()]


@AppRoute(routes, ['/products'])
class ViewProductList:
    """
    Контроллер списка продуктов
    """

    def __call__(self, request):
        print()
        return '200 OK', [render('products.html', templates_path,
                                 products_list=site.products).encode()]


@AppRoute(routes, ['/product_create'])
class ViewProductCreate:
    """
    Контроллера создания продукта (оставил почти без изменения)
    """

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
