

class Error(Exception):
	def __str__(self):
		return self.args[0].format(*self.args[1:])


class Lit(object):
	def __init__(self, val):	
		self.val = val
		
	def get_val(self):
		return self.val
	
	def get(self): 
		return self.val
	
		
	def __str__(self):
		return "\"{}\"".format(self.val)

class Atm(object):
	def __init__(self, val):	
		self.val = val
		
	def get_id(self): 
		return self.val
	
	def get(self): 
		return self.val
		
		
	def __str__(self):
		return "{}".format(self.val)
		#return "Sym({})".format(Sym.symtab.get_name(self.id))


	
class Seq(object):
	def __init__(self, *xs):	
		self.xs = xs
		
	def get_list(self):
		return self.xs
	
	def get(self):
		return self.xs
	
	
	def __str__(self):
		return "({})".format(' '.join(str(x) for x in self.xs))
		#return "Lst([{}])".format(','.join(str(x) for x in self.xs))





