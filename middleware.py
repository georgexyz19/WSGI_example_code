
from sys import exc_info
from traceback import format_tb

# from cgi import parse_qs, escape
from urllib.parse import parse_qs   # for python 3.8
from html import escape

'''
 sys.exc_info() : This function returns a tuple of three values that give information 
 about the exception that is currently being handled. 

If no exception is being handled anywhere on the stack, a tuple containing three None 
values is returned. Otherwise, the values returned are (type, value, traceback). 
Their meanings are: type gets the type of the exception being handled (a subclass of 
BaseException); value gets the exception instance (an instance of the exception type); 
traceback gets a traceback object (see the Reference Manual) which encapsulates 
the call stack at the point where the exception originally occurred.

'''

class ExceptionMiddleware(object):
    '''The middleware we use.'''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        '''call the application can catch exceptions'''
        appiter = None

        try:
            appiter = self.app(environ, start_response)
            for item in appiter:
                yield item

        except:
            e_type, e_value, tb = exc_info()
            traceback = ['Traceback (most recent call last):']
            traceback += format_tb(tb)
            traceback.append('%s: %s' % (e_type.__name__, e_value))

            try:
                start_response('500 INTERNAL SERVER ERROR', [
                  ('Content-Type', 'text/plain')] )
            except:
                pass

            yield '<br/>'.join(traceback).encode('utf-8')

        if hasattr(appiter, 'close'):
            appiter.close()

'''
http://localhost:8080/
Hello World

http://localhost:8080/?subject=john
Result: Traceback (most recent call last):
File "middleware.py", line 31, in __call__ appiter = self.app(environ, start_response)
File "middleware.py", line 68, in hello_world raise ValueError('Cannot be john')
ValueError: Cannot be john
'''

def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0])
    else:
        subject = 'world'

    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = 'Hello {}'.format(subject)

    if subject == 'john':
        raise ValueError('Cannot be john')

    # a = 10 / 0  # create divide-by-0 exception

    return [mystr.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = ExceptionMiddleware(hello_world)
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
