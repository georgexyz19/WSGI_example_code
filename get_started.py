
from cgi import parse_qs, escape

# escape see SO 1061697, < to &lt; > to &gt; and & to &amp;
# second quote parameter, escape double quote char (") so you can use the 
#   resulting value in a XML/HTML attribute.  html.escape does the same except
#   that quote defaults to True
# 
# parse_qs also has SO 2886611

def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0])
    else:
        subject = 'world'

    start_response('200 OK', [('Content-Type', 'text/html')])
    mystr = 'Hello {}'.format(subject)
    return [mystr.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, hello_world)
    srv.serve_forever()