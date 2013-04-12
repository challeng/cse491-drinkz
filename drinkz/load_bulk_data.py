"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package
from . import recipes

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """

    x = []
    n = 0

    

    #for mfg, name, typ in new_reader:
     #   n += 1
      #  db.add_bottle_type(mfg, name, typ)

    #reader = csv.reader(fp)
    new_reader = data_reader(fp)


    for line in new_reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
        n += 1
        db.add_bottle_type(mfg, name, typ)
 



    return n

def load_recipes(fp):
    reader = csv.reader(fp)
    a = []
    ingredients = []
    n=0


    for line in reader:
        try:
            #a.append(line)
            a = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue


        name = a[0]
        counter = 0
        for data in a:
            #recipe name
            if counter == 0:
                counter = counter+1
                continue
            #odd, its the type
            if counter%2 == 1:
                ing = (a[counter], a[counter+1])
                ingredients.append(ing)


            counter = counter+1


         
        r = recipes.create(name, ingredients)
        if r:
            n +=1
        db.add_recipe(r)

    return n


def data_reader(fp):
    reader = csv.reader(fp)
 

    for line in reader:
        if len(line) == 0 or line[0].startswith('#'):
            #raise db.BadData("bad Data!")
            continue

        print len(line)

        yield line


def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """

    reader = csv.reader(fp)


    x = []
    n = 0


    new_reader = data_reader(fp)


    for line in new_reader:
        try:
            (mfg, name, amount) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
        n += 1
        db.add_bottle_type(mfg, name, 'test_type')
        db.add_to_inventory(mfg, name, amount)




    return n

    for (mfg, name, amount) in reader:
        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n

    # FIXME

