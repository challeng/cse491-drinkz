from . import db

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

	def __eq__(self, other):
		if self.name == other.name and self.ingredients == other.ingredients:
			return True
		return False

	def need_ingredients(self):
		needed_ingredients = []
		for i in self.ingredients:
			typ = i[0]
			amount = i[1]
			bottle = db._find_bottle_from_type(typ)
			newAmount = 0

			print bottle
			#no bottle
			if bottle == []:
				needed_ingredients.append((typ, db.convert_to_ml(amount)))
				continue
			#one bottle
			elif len(bottle) == 1:
				mfg = bottle[0][0]
				liquor = bottle[0][1]
				newAmount = db.get_liquor_amount(mfg, liquor)
			#more bottles
			else:
				for b in bottle:
					mfg = b[0]
					liquor = b[1]
					if db.get_liquor_amount(mfg, liquor) > newAmount:
						newAmount = db.get_liquor_amount(mfg, liquor)

				#mfg = bottle[0]
				#liquor = bottle[1]


			#if we dont have enough
			if db.convert_to_ml(amount) > newAmount:
				print "amount more"
				print db.convert_to_ml(amount)
				print newAmount
				needed = db.convert_to_ml(amount) - newAmount
				needed_ingredients.append((typ, needed))

			continue


		return needed_ingredients

				

				


	
		