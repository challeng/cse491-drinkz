from . import db.py

class Recipe(object):
	"""
	docstring for Recipe
	"""
	name = ""
	ingredients = []
	def __init__(self, name, ingredients):
		super(Recipe, self).__init__()
		self.name = name
		self.ingredients = ingredients

	def need_ingredients(inventory_db):
		needed_ingredients = []
		for i in ingredients:
			typ = i[0]
			amount = i[1]
			bottle = db._find_bottle_from_type(typ)
			mfg = bottle[0]
			liquor = bottle[1]

			for k,v in inventory_db:
				#if bottle exists
				if (mfg, liquor) == k:
					#if we dont have enough
					if amounts > v:
						 needed = a - v
						 needed_ingredients.add((typ, needed))
				#bottle doesnt exist
				else:
					needed_ingredients.add((typ, amount))

		return needed_ingredients

				

				


	
		