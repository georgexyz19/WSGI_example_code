
# from cgi import parse_qs, escape  # removed in python 3.8
from urllib.parse import parse_qs   # for python 3.8
from html import escape

# SO - Stackoverflow.com
# escape see SO 1061697, < to &lt; > to &gt; and & to &amp;
# a second 'quote' parameter, escape double quote char (") so you can use the 
#   resulting value in a XML/HTML attribute.  html.escape does the same except
#   that quote defaults to True
# 
# parse_qs also has SO 2886611, qs - query string, removed in python 3.8
#   data are returned as a dictionary

# test cases, SEE the print output on line 19
# http://localhost:8080/
# http://localhost:8080/?subject=john
# http://localhost:8080/?subject=john&name=george
# http://localhost:8080/?subject=john&subject=george


# update 10/31/2020
# you can run the app with a real WSGI server like gunicorn
# in you virtual env `pip install gunicorn`
# run command `gunicorn -w 4 get_started:hello_world`
# get_started file name or py module name
# the environ dict has 29 keys running with gunicorn vs 82 keys w/ wsgiref

# update 3/19/2021
# The browser will send a second request automatically
# 127.0.0.1 - - [19/Mar/2021 11:12:00] "GET /favicon.ico HTTP/1.1" 200 11

# The QUERY_STRING key -> value look like this `subject=john&name=george` 
#  for case number 3 above


def hello_world(environ, start_response):

    # check environ values, it is a dict
    print('\nStart printing dict environ')
    d = environ
    for i, (k, v) in enumerate(sorted(d.items()), start=1):
        print(i, k, '->', v)
    print('End printing dict environ\n')

    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    ### parameters is {'subject': ['john'], 'name': ['george']} case # 3
    
    print('parameters is {}'.format(parameters))
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
    print('wsgiref is serving the WSGI app ......')
    srv.serve_forever()
