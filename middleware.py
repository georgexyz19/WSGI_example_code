
from sys import exc_info
from traceback import format_tb

from cgi import parse_qs, escape


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
                
            yield '\n'.join(traceback)
            
        if hasattr(appiter, 'close'):
            appiter.close()
            
            
def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0])
    else:
        subject = 'world'
        
    # a = 10 / 0  # to create divide-by-0 exception

    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = 'Hello {}'.format(subject)
    return [mystr.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = ExceptionMiddleware(hello_world)
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
