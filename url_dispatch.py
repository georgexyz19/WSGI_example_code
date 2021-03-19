import re
# from cgi import escape   # for Python 3.8
from html import escape

# Test cases:
# http://localhost:8080/
# http://localhost:8080/hello/
# http://localhost:8080/hello/john

# Use gunicorn, the environ variable is more clear
# http://127.0.0.1:8000/foo?subject=john
# PATH_INFO -> /foo
# QUERY_STRING -> subject=john

def index(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = '''Hello World Application
        This is the Hello World application: </br>

            <a href='/hello/'>hello</a>
        '''
    return [mystr.encode('utf-8')]


def hello(environ, start_response):
    args = environ['myapp.url_args']
    if args:
        subject = escape(args[0])
    else:
        subject = 'World'
    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = 'Hello %(subject)s' % {'subject': subject}
    return [mystr.encode('utf-8')]


def not_found(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = 'Not Found'
    return [mystr.encode('utf-8')]


urls = [
    (r'^$', index),
    (r'^hello/?$', hello),
    (r'^hello/(.+)$', hello),
]


# https://docs.python.org/3/library/re.html?highlight=regular%20expression#match-objects
# this link shows what match.groups is
# example :
# >>> m = re.match(r'(\d+)\.(\d+)', '24.1632')
# >>> m.groups()
# ('24', '1632')
# >>> m.group()
# '24.1632'
# >>> m.group(0)
# '24.1632'
# >>> m.group(1)
# '24'
# >>> m.group(2)
# '1632
#


def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    print('path is {}'.format(path))
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['myapp.url_args'] = match.groups()  # groups returns a tuple        
            return callback(environ, start_response)
    return not_found(environ, start_response)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    print('wsgiref is serving the WSGI app ......')
    srv.serve_forever()
