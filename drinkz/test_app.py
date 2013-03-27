import app
import urllib
import db
import recipes

def make_db():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')
    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

    db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
    db.add_to_inventory('Gray Goose', 'vodka', '1 liter')
    db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
    db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

    r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'), ('vermouth', '1.5 oz')])
    db.add_recipe(r)
    r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
    db.add_recipe(r)

def test_recipes():
    make_db();

    environ = {}
    environ['PATH_INFO'] = '/recipes'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']

    assert status == '200 OK'
    assert text.find('scotch on the rocks') != -1, text
    assert text.find('vodka martini') != -1, text
    assert text.find('vomit inducing martini') != -1, text



# def test_index():
#     environ = {}
#     environ['PATH_INFO'] = '/'
    
#     d = {}
#     def my_start_response(s, h, return_in=d):
#         d['status'] = s
#         d['headers'] = h

#     app_obj = app.SimpleApp()
#     results = app_obj(environ, my_start_response)

#     text = "".join(results)
#     status, headers = d['status'], d['headers']
    
#     assert text.find('Visit:') != -1, text
#     assert ('Content-type', 'text/html') in headers
#     assert status == '200 OK'

# def test_form_recv():
#     environ = {}
#     environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO',
#                                                     lastname='BAR'))
#     environ['PATH_INFO'] = '/recv'

#     d = {}
#     def my_start_response(s, h, return_in=d):
#         d['status'] = s
#         d['headers'] = h

#     app_obj = app.SimpleApp()
#     results = app_obj(environ, my_start_response)
    
#     text = "".join(results)
#     status = d['status']
#     headers = d['headers']

#     assert text.find("First name: FOO; last name: BAR.") != -1, text
#     assert ('Content-type', 'text/html') in headers
#     assert status == '200 OK'