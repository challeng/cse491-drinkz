"""
Database functionality for drinkz information.

I choose to use a set to store my recipes.
It seemed like we would not need more then one of each recipe
and also that we did not need something like a dictionary because
there are no key,value pairs.
"""

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
_recipe_db = set()

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set([])
    _inventory_db = {}
    _recipe_db = set()

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."

    _bottle_types_db.add((mfg, liquor, typ))


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def _find_bottle_from_type(typ):
    final = []
    for(m, l, t) in _bottle_types_db:
        if typ == t:
            final.append((m, l, t))
            continue
    return final

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    #print mfg

    # just add it to the inventory database as a tuple, for now.
    #_inventory_db.append((mfg, liquor, amount))
    #print "adding" + amount
    amount = convert_to_ml(amount)

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] = _inventory_db[(mfg, liquor)] + amount
    else:
        _inventory_db[(mfg, liquor)] = amount


def check_inventory(mfg, liquor):

    for k,v in _inventory_db.iteritems():
        m = k[0]
        l = k[1]
        if mfg == m and liquor == l:
            return True
        

    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = []
    for k in _inventory_db:
        m = k[0]
        l = k[1]
        amount = _inventory_db[k]
        if mfg == m and liquor == l:
            amounts.append(amount)

    total = 0
    for amount in amounts:
        total = total + float(amount)

    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for k,v in _inventory_db.iteritems():
        m = k[0]
        l = k[1]
        a = v
        yield m, l

def get_liquor_types():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l, t) in _bottle_types_db:
        yield m, l, t



def add_recipe(r):
    _recipe_db.add(r)

def get_recipe(name):
    for r in _recipe_db:
        if r.name == name:
            return r


def get_all_recipes():
    for r in _recipe_db:
        yield r


def convert_to_ml(amount):
    if amount.endswith("oz"):
        amount = amount[:-2]
        amount = float(amount) * 29.5735
    elif amount.endswith("ml"):
        amount = amount[:-2]
    elif "gallon" in amount:
        amount = amount[:-6]
        amount = float(amount) * 3785.41
    elif "liter" in amount:
        amount = amount[:-5]
        amount = float(amount) * 1000
    else:
        amount = -1;

    amount = float(amount)
    return amount    











