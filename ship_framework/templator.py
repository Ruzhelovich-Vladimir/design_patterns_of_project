from jinja2 import Template


def render(path, **kwargs):

    with open(path, encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)


if __name__ == '__main__':

    goods = [{'name': f'Товар #{inx}', 'price': inx*100} for inx in range(1, 5)]
    print(render(path='test.html', title='Test title', goods=goods))

