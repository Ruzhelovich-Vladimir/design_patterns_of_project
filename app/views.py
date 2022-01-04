from ship_framework.templator import render

templates_path = 'app/templates'

class ViewIndex:
    def __call__(self, request):
        return '200 OK', [render('index.html', templates_path).encode()]

class ViewWork:
    def __call__(self, request):
        return '200 OK', [render('work.html', templates_path).encode()]

class ViewAbout:
    def __call__(self, request):
        return '200 OK', [render('about.html', templates_path).encode()]

class ViewBlog:
    def __call__(self, request):

        blogs = [
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
              <b>Spider-Man</b> is a fictional character, a comic book superhero that appears in comic books published by Marvel Comics. Created by writer-editor Stan Lee and writer-artist Steve Ditko, he first appeared in Amazing Fantasy #15 (cover-dated Aug. 1962).
              Lee and Ditko conceived the character as an orphan being raised by his Aunt May and Uncle Ben, and as a teenager, having to deal with the normal struggles of adolescence in addition to those of a costumed crimefighter. 
              """
              },
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
                      <b>Spider-Man</b> is a fictional character, a comic book superhero that appears in comic books published by Marvel Comics. Created by writer-editor Stan Lee and writer-artist Steve Ditko, he first appeared in Amazing Fantasy #15 (cover-dated Aug. 1962).
                      Lee and Ditko conceived the character as an orphan being raised by his Aunt May and Uncle Ben, and as a teenager, having to deal with the normal struggles of adolescence in addition to those of a costumed crimefighter. 
                      """
            },
            {
                "author": "Stanley Stinson",
                "date": "January 18, 2014",
                "title": "The Amazing Spiderman",
                "text": """
                      <b>Spider-Man</b> is a fictional character, a comic book superhero that appears in comic books published by Marvel Comics. Created by writer-editor Stan Lee and writer-artist Steve Ditko, he first appeared in Amazing Fantasy #15 (cover-dated Aug. 1962).
                      Lee and Ditko conceived the character as an orphan being raised by his Aunt May and Uncle Ben, and as a teenager, having to deal with the normal struggles of adolescence in addition to those of a costumed crimefighter. 
                      """
            }
        ]

        return '200 OK', [render('blog.html', templates_path, blogs=blogs).encode()]

class ViewContact:
    def __call__(self, request):
        return '200 OK', [render('contact.html', templates_path).encode()]
