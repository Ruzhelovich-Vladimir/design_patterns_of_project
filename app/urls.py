from app.views import ViewIndex, ViewWork, ViewAbout, ViewBlog, ViewContact, \
    ViewCategoryList, ViewCategoryCreate, ViewProductList, ViewProductCreate, \
    ViewProductCopy

routes = {
    '/': ViewIndex(),
    '/index': ViewIndex(),
    '/work': ViewWork(),
    '/about': ViewAbout(),
    '/blog': ViewBlog(),
    '/contact': ViewContact(),
    '/categories': ViewCategoryList(),
    '/category_create': ViewCategoryCreate(),
    '/products': ViewProductList(),
    '/product_create': ViewProductCreate(),
    '/product_copy': ViewProductCopy()
}
