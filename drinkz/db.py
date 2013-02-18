"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = set([])
#_new_bottle_types_db = []
_inventory_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set([])
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    #print mfg

    # just add it to the inventory database as a tuple, for now.
    #_inventory_db.append((mfg, liquor, amount))
    #print "adding" + amount
    if amount.endswith("oz"):
        amount = amount[:-2]
        amount = float(amount) * 29.5735
    elif amount.endswith("ml"):
        amount = amount[:-2]

    amount = float(amount)

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] = str(int(_inventory_db[(mfg, liquor)][:-2]) + amount) + " ml"
    else:
        _inventory_db[(mfg, liquor)] = str(int(amount)) + " ml"


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
            amount = str(amount)[:-2]
            amounts.append(amount)

    total = 0
    for amount in amounts:
        total = total + float(amount)

    return str(int(total)) +" ml"

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for k,v in _inventory_db.iteritems():
        m = k[0]
        l = k[1]
        a = v
        yield m, l, a

def get_liquor_types():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l, t) in _bottle_types_db:
        yield m, l, t
