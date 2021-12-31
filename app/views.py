from ship_framework.templator import render


class ViewIndex:
    def __call__(self, request):
        return '200 OK', [render('app/template/index.html').encode()]

class ViewWork:
    def __call__(self, request):
        return '200 OK', [render('app/template/work.html').encode()]

class ViewAbout:
    def __call__(self, request):
        return '200 OK', [render('app/template/about.html').encode()]

class ViewBlog:
    def __call__(self, request):
        return '200 OK', [render('app/template/blog.html').encode()]

class ViewContact:
    def __call__(self, request):
        return '200 OK', [render('app/template/contact.html').encode()]
