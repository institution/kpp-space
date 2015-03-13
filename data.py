
class Error(Exception):
	pass


class Env:
	def __init__(self, par):	
		self.tab = dict()
		self.par = par
		
	def get(self, sym):
		id = sym.get_id()
		if id in self.tab:
			return self.tab[id]
		else:
			if self.par is not None:
				return self.par.get(sym)
			else:
				raise Error('symbol not found: '+str(sym))
	
	def set(self, sym, x):
		id = sym.get_id()
		if id in self.tab:
			raise Error('already defined: {}'.format(id))
		self.tab[id] = x
	
	def __str__(self):
		rs = []
		for k,v in self.tab.items():
			rs.append("{}={}".format(str(Sym(k)), str(v)))
		return "Env({})".format(';'.join(rs)) + '+par'
			


class Nil: 
	def __init__(self):	
		pass
		
	def __str__(self):
		return "NIL"
		
		
class Val:
	def __init__(self, val):	
		self.val = val
		
	def get_val(self):
		return self.val
		
	def __str__(self):
		return "{}".format(self.val)
		#return "Val({})".format(self.val)

class Lit:
	def __init__(self, val):	
		self.val = val
		
	def get_val(self):
		return self.val
	
class Ref:
	def __init__(self, func):	
		self.func = func
		
class Vau:
	def __init__(self, func):	
		self.func = func
		
	def get_func(self): 
		return self.func
	
	def __str__(self):
		return "Vau({})".format(self.func)
	
class Sym:
	def __init__(self, id):	
		self.id = id
		
	def get_id(self): 
		return self.id
		
	def __str__(self):
		return "{}".format(Sym.symtab.get_name(self.id))
		#return "Sym({})".format(Sym.symtab.get_name(self.id))
	
class Lst:
	def __init__(self, xs):	
		self.xs = xs
		
	def get_list(self):
		return self.xs
	
	def __str__(self):
		return "({})".format(' '.join(str(x) for x in self.xs))
		#return "Lst([{}])".format(','.join(str(x) for x in self.xs))
