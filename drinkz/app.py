#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson

from drinkz import db, recipes
#import db
import imp

#CALL make-test-database then check that it works
scriptpath = 'bin/make-test-database'
filename = 'db.txt'
module = imp.load_source('llt', scriptpath)
exit_code = module.main([scriptpath, filename])

db.load_db(filename)




dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/index' : 'index'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = """\

<head><title>Index</title>
<style type="text/css">
h1 {color:red;}
</style>
<script>
function myFunction()
{
alert("I am a really cool alert box!");
}
</script>
</head>
<body>
<h1>Index</h1>
<input type="button" onclick="myFunction()" value="Show alert box">
        
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<a href='inventory'>Inventory</a>
<a href='recipes'>Recipes</a>
<a href='index'>Index</a>
<p>
<img src='/helmet'>
</body>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        data = """\

<head><title>Inventory</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Inventory</h1>
        
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<a href='inventory'>Inventory</a>
<a href='recipes'>Recipes</a>
<a href='index'>Index</a>
<p>
<img src='/helmet'>
</body>
"""

        for m,l in db.get_liquor_inventory():
            data+= "<li>"
            data+= m
            data+= ", "
            data+= str(db.get_liquor_amount(m, l))
            data+= " ml"
            data+= "</li>\n"

        data+= "</ul>"

        start_response('200 OK', list(html_headers))
        return [data]

    def recipes(self, environ, start_response):
        data = """\

<head><title>Recipes</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Recipes</h1>
        
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<a href='inventory'>Inventory</a>
<a href='recipes'>Recipes</a>
<a href='index'>Index</a>
<p>
<img src='/helmet'>
</body>
"""
        
        for r in db.get_all_recipes():
            data+= "<li>"
            data+= r.name
            if r.need_ingredients() == []:
                data+=", Have all ingredients."
            else:
                data+= ", Need more ingredients."

            data+= "</li>\n"
        data+= "</ul>"

        start_response('200 OK', list(html_headers))
        return [data]
        
    def somefile(self, environ, start_response):
        content_type = 'text/html'
        data = """\

<head><title>Content</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Content</h1>
        
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<a href='inventory'>Inventory</a>
<a href='recipes'>Recipes</a>
<a href='index'>Index</a>
<p>
<img src='/helmet'>
</body>
"""

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = """\
        

<head><title>Error</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Error</h1>

Couldn't find your stuff.
</body>
"""
        
       
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['amount'][0]
        num_amount = db.convert_to_ml(amount);

        content_type = 'text/html'

        if(num_amount != -1):
            data1 = "Amount in ML: %d; <a href='./'>return to index</a>" % (num_amount)
        else:
            data1 = "Unknown Units; <a href='./'>return to index</a>"

        data = """\

<head><title>Form Results</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Form Results</h1>"""

        data += data1
        data += """
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<a href='inventory'>Inventory</a>
<a href='recipes'>Recipes</a>
<a href='index'>Index</a>
<p>
<img src='/helmet'>
</body>
"""


        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
    
def form():
    return """
<form action='recv'>
Input amount to convert to ML <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()