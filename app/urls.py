from app.views import ViewIndex, ViewWork, ViewAbout, ViewBlog, ViewContact

routes = {
    '/': ViewIndex(),
    '/index': ViewIndex(),
    '/work': ViewWork(),
    '/about': ViewAbout(),
    '/blog': ViewBlog(),
    '/contact': ViewContact()
}
