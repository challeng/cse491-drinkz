from . import db

def create(name, ingredients):
	r = Recipe(name, ingredients)
	return r

class Recipe(object):
	"""
	docstring for Recipe
	"""
	name = ""
	ingredients = []
	trueRating = 0;
	rating = -1
	ratingCount = 0
	def __init__(self, name, ingredients):
		super(Recipe, self).__init__()
		self.name = name
		self.ingredients = ingredients



	def __eq__(self, other):
		if self.name == other.name and self.ingredients == other.ingredients:
			return True
		return False

	def rate(self, r):
		if int(r) > 5 or int(r) < 0:
			return

		if self.rating == -1:
			
			self.ratingCount = 1
			self.rating = int(r)
		else:
			
			self.ratingCount += 1
			self.rating += int(r)


		if self.rating == 0 or self.ratingCount == 0:
			pass
		else:
			self.trueRating = float(self.rating) / float(self.ratingCount)


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

				

				


	
		