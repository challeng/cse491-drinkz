#! /usr/bin/env python

import os
from drinkz import db, recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

import imp

#CALL make-test-database then check that it works
scriptpath = 'bin/make-test-database'
module = imp.load_source('llt', scriptpath)
exit_code = module.main([scriptpath, 'jim.txt'])


###

fp = open('html/index.html', 'w')
print >>fp, """
<p><a href='index.html'>this is a relative link to index!</a></p>
<p><a href='recipes.html'>this is a relative link to recipes!</a></p>
<p><a href='inventory.html'>this is a relative link to inventory!</a></p>
<p><a href='liquor_types.html'>this is a relative link to liquor types!</a></p>
<h1>Hello, world!(Index)</h1>
"""




fp.close()

###

fp = open('html/recipes.html', 'w')

print >>fp, """
<p><a href='index.html'>this is a relative link to index!</a></p>
<p><a href='recipes.html'>this is a relative link to recipes!</a></p>
<p><a href='inventory.html'>this is a relative link to inventory!</a></p>
<p><a href='liquor_types.html'>this is a relative link to liquor types!</a></p>
<h1>Recipes</h1>
<ul>
"""
for r in db.get_all_recipes():
  print >>fp, "<li>"
  print >>fp, r.name
  if r.need_ingredients() == []:
    print >>fp, ", Have all ingredients."
  else:
    print >>fp, ", Need more ingredients."

  print >>fp, "</li>"

print >>fp, "</ul>"


fp.close()

###

fp = open('html/inventory.html', 'w')

print >>fp, """
<p><a href='index.html'>this is a relative link to index!</a></p>
<p><a href='recipes.html'>this is a relative link to recipes!</a></p>
<p><a href='inventory.html'>this is a relative link to inventory!</a></p>
<p><a href='liquor_types.html'>this is a relative link to liquor types!</a></p>
<h1>Inventory</h1>
<ul>
"""

for m,l in db.get_liquor_inventory():
  print >>fp, "<li>"
  print >>fp, m
  print >>fp, ", "
  print >>fp, db.get_liquor_amount(m, l)
  print >>fp, " ml"
  print >>fp, "</li>"

print >>fp, "</ul>"

fp.close()

###

fp = open('html/liquor_types.html', 'w')

print >>fp, """
<p><a href='index.html'>this is a relative link to index!</a></p>
<p><a href='recipes.html'>this is a relative link to recipes!</a></p>
<p><a href='inventory.html'>this is a relative link to inventory!</a></p>
<p><a href='liquor_types.html'>this is a relative link to liquor types!</a></p>
<h1>Liquor Types</h1>
<ul>
"""

for m,l,t in db.get_liquor_types():
  print >>fp, "<li>"
  print >>fp, m + ", " + l + ", " + t
  print >>fp, "</li>"

print >>fp, "</ul>"

fp.close()

###
