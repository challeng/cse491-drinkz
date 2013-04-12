#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson

from drinkz import db, recipes
#import db
import imp

#CALL make-test-database then check that it works
#scriptpath = 'bin/make-test-database'
filename = 'db.txt'
#module = imp.load_source('llt', scriptpath)
#exit_code = module.main([scriptpath, filename])

db.load_db(filename)




dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/liquor_type_form' : 'lt_form',
    '/liquor_inv_form' : 'li_form',
    '/recipe_form' : 'recipe_form',
    '/recv' : 'recv',
    '/lt_recv' : 'lt_recv',
    '/li_recv' : 'li_recv',
    '/recipe_recv' : 'recipe_recv',
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
<a href='liquor_type_form'>a form for liquor type...</a>
<a href='liquor_inv_form'>a form for liquor inventory...</a>
<a href='recipe_form'>a form for recipes...</a>
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

    def lt_form(self, environ, start_response):
        data = lt_form()

        start_response('200 OK', list(html_headers))
        return [data]

    def li_form(self, environ, start_response):
        data = li_form()

        start_response('200 OK', list(html_headers))
        return [data]

    def recipe_form(self, environ, start_response):
        data = recipe_form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        print results

        amount = results['amount'][0]

        print amount
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


    def lt_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        typ = results['typ'][0]

        print mfg
        print liquor
        print typ

        db.add_bottle_type(mfg, liquor, typ)

        content_type = 'text/html'

        

        data = """\

<head><title>Form Results</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Form Results</h1>"""

        data += "Mfg: " + mfg
        data += "Liquor: " + liquor
        data += "Type: " + typ
        data += """
Visit:

<a href='index'>Index</a>

</body>
"""


        start_response('200 OK', list(html_headers))
        return [data]


    def li_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        amount = results['amount'][0]

        num_amount = db.convert_to_ml(amount);

        content_type = 'text/html'

        if(num_amount != -1):
            amount = "Amount in ML: %d" % (num_amount)
        else:
            amount = "Unknown Units"

        db.add_to_inventory(mfg,liquor,amount)
        



        data = """\

<head><title>Form Results</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Form Results</h1>"""

        data += "Mfg: " + mfg
        data += "Liquor: " + liquor
        data += amount
        data += """
Visit:

<a href='index'>Index</a>

"""


        start_response('200 OK', list(html_headers))
        return [data]


    def recipe_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        ingredients = results['ingredients'][0]
        ingredients = ingredients.split()
        ing = []

        counter = 0
        for i in ingredients:
            #first
            if counter%2 == 0 and counter+1 < len(ingredients):
                i = (ingredients[counter], ingredients[counter+1])
                ing.append(i)

            counter += 1

        r = recipes.create(name, ing)    
        db.add_recipe(r)



        content_type = 'text/html'

        

        data = """\

<head><title>Form Results</title>
<style type="text/css">
h1 {color:red;}
</style>
</head>
<body>
<h1>Form Results</h1>"""

        data += "Name: " + name
        data += "Ingredients: "
        for i in ing:
            for parts in i:
                data += parts +"\n"
        data += """
Visit:
<a href='index'>Index</a>

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

    def rpc_lt(self, mfg, liquor, typ):
        db.add_bottle_type(mfg, liquor, typ)
        print db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
        return mfg + " " + liquor + " " + typ

    def rpc_li(self, mfg, liquor, amount):
        #new_amount = db.convert_to_ml(amount)
        db.add_to_inventory(mfg, liquor, amount)
        return mfg + " " + liquor + " " + amount

    def rpc_recipe(self, name, ingredients):
        ingredients = ingredients.split()
        ing = []

        counter = 0
        for i in ingredients:
            #first
            if counter%2 == 0 and counter+1 < len(ingredients):
                i = (ingredients[counter], ingredients[counter+1])
                ing.append(i)

            counter += 1

        r = recipes.create(name, ing) 
        db.add_recipe(r)
        data = name + " Ingredients: "
        for i in ing:
            for parts in i:
                data += parts +" "
            data += "\n"
        return data
    
def form():
    return """
<form action='recv'>
Input amount to convert to ML <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
"""

def lt_form():
    return """
<form action='lt_recv'>
Input liquor mfg <input type='text' name='mfg' size'20'>
Input liquor name <input type='text' name='liquor' size'20'>
Input liquor type <input type='text' name='typ' size'20'>
<input type='submit'>
</form>
"""

def li_form():
    return """
<form action='li_recv'>
Input liquor mfg <input type='text' name='mfg' size'20'>
Input liquor name <input type='text' name='liquor' size'20'>
Input liquor amount <input type='text' name='amount' size'20'>
<input type='submit'>
</form>
"""

def recipe_form():
    return """
<form action='recipe_recv'>
Input recipe name <input type='text' name='name' size'20'>
Input recipe ingredients <input type='text' name='ingredients' size'20'>
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