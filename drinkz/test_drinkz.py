"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
import os
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data


#THESE THREE RPC TESTS DEPEND ON SERVER NAME WHICH I CHANGE ACOORIDNG TO WHAT I GET WHEN I RUN run-web
server_name = "http://host-21-166.miellan.clients.pavlovmedia.com:9481/"

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'


def test_rpc_lt():
    db._reset_db()

    #os.system("python drinkz/json-rpc-client.py " + server_name)
    print db.len_bottle_types()
    #assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')


def test_rpc_li():
    db._reset_db()

    #os.system("python drinkz/json-rpc-client.py " + server_name)
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')

    print amount
    #assert amount == 100

def test_rpc_rec():
    db._reset_db()

    #os.system("python drinkz/json-rpc-client.py " + server_name)
    r = db.get_recipe("scotch on the rocks")
    #assert r != False


def test_total_ml_oz():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 oz')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '2000 ml')

    assert db.get_liquor_amount('Johnnie Walker', 'Black Label') == 31573.5


def test_total_ml():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '2000 ml')

    assert db.get_liquor_amount('Johnnie Walker', 'Black Label') == 3000

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    print n

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_inventory_comments():
    db._reset_db()

    file1 = open('test-data/bottle-types-data-4.txt','r')

    n = load_bulk_data.load_inventory(file1)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_inventory_newline():
    db._reset_db()

    file1 = open('test-data/bottle-types-data-3.txt','r')

    #n2 = load_bulk_data.load_bottle_types(file1)
    n = load_bulk_data.load_inventory(file1)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert db._check_bottle_type_exists('Jim Challenger', 'Brown Label')
    assert n == 2, n


def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_bulk_load_bottle_types_1():


    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)


    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_bottle_types_comments():
    db._reset_db()

    file1 = open('test-data/bottle-types-data-1.txt','r')

    n = load_bulk_data.load_bottle_types(file1)
    print n


    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_bulk_load_recipes_1():
    db._reset_db()

    file1 = open('test-data/recipes-data-1.txt', 'r')

    n = load_bulk_data.load_recipes(file1)
    print n

    assert n == 1, n

def test_bulk_load_recipes_2():
    db._reset_db()

    file1 = open('test-data/recipes-data-2.txt', 'r')

    n = load_bulk_data.load_recipes(file1)
    print n

    assert n == 2, n


def test_bulk_load_bottle_types_newline():
    db._reset_db()

    file1 = open('test-data/bottle-types-data-2.txt','r')

    n = load_bulk_data.load_bottle_types(file1)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert db._check_bottle_type_exists('Jim Challenger', 'Brown Label')
    assert n == 2, n    

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code

def test_script_load_inventory_incorrect():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-4.txt'])

    assert exit_code == -1, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x

    #assert False, "this needs to be implemented."




