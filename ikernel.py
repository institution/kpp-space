import types
from parser2 import parse, Lit, Seq, Atm, Error

Sym = Atm
Lst = Seq

'''
def tokenize(x):
	if isa(x, Seq):
		ls = []
		ls.append('(')
		for y in x.get():
			ls.extend(tokenize(y))
		ls.append(')')
		return ls
		
	elif isa(x, Lit):
		return [str(x)]
		
	elif isa(x, Atm):
		return [str(x)]
		
	else:
		return [repr(x)]


def ppretty(ts):
	for t in ts:
		if t == '('
'''

'''
Literal
ptr to (length,string)

Atom
ptr to string (alt. ptr to integer)

Sequence (Array)


Nil

Int
integer

Str
(ptr to array of char, length)

code -> simplification -> static-eval -> precompiled code (llvm) -> arch optimization -> compiled code (binary)

'''


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
	
	def get(self):
		return self.val
	
		
	def __str__(self):
		return "{}".format(self.val)


class Int(Val):
	pass

class Str(Val):
	pass


	
#class Ref:
#	def __init__(self, func):	
#		self.func = func
		
class Vau:
	def __init__(self, func):	
		self.func = func
		
	def get_func(self): 
		return self.func
		
	def get(self): 
		return self.func

	
	def __str__(self):
		return "Vau({})".format(self.func)




class Env:
	def __init__(self, par):	
		self.tab = dict()
		self.par = par
		
	def get(self, atm):
		key = atm.get()
		if key in self.tab:
			return self.tab[key]
		else:
			if self.par is not None:
				return self.par.get(atm)
			else:
				raise Error('symbol not found: '+str(atm))
	
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
			




def isa(x,t):
	return type(x) == t

def print_(env, a):
	print("#-> {}".format(eval_(env, a)))
	return Nil()
		
def begin(env, *args):
	loc = Env(env)
	
	r = Nil()
	for a in args:
		r = eval_(loc, a)
		
		
	return r

def def_(env, a, b):
	env.set(a, eval_(env, b))
	return Nil()
	
def match_arg(expr):
	if isa(expr, Seq):
		ls = expr.get_list()
		if len(ls) == 2:
			s = ls[0]
			if isa(s, Atm):
				if s.get() == 'arg':
					return True
	return False
	
	
def argblock(env, *body):
	return eval_(env, parse_argable_block(env, *body))
	
def parse_argable_block(env, *expr):
	# block with arg(s) -> lambda
	args = []
	body = []
	for sube in expr:
		if match_arg(sube):
			args.append(sube.get_list()[1])
		else:
			body.append(sube)
			
	return Lst(Atm('lambda'), Lst(*args), Lst(Atm('do'), *body))
	
	
	
	
def add(env, a, b):	
	return Val(eval_(env, a).get_val() + eval_(env, b).get_val())
	
def sub(env, a, b):	
	return Val(eval_(env, a).get_val() - eval_(env, b).get_val())
	



class Closure:
	def __init__(self, env, s_args, s_env, s_body):
		self.env = env
		self.s_args = s_args
		self.s_env = s_env
		self.s_body = s_body
			
	def __call__(self, env, *args):
		
		if len(self.s_args.get_list()) != len(args):
			import ipdb; ipdb.set_trace()
			assert 0
		
		# eval body in lexical env + args
		local = Env(self.env)
		
		for sym, arg in zip(self.s_args.get_list(), args):
			local.set(sym, arg)
					
		# pass dynamic scope
		local.set(self.s_env, env)
		
		return eval_(local, self.s_body)


def vau(env, decl, esym, body):
	return Vau(Closure(env, decl, esym, body))

def list_(env, *args):	
	return Lst(*[eval_(env, x) for x in args])

def quote(env, arg):
	return arg

def concat(env, *args):
	ls = []
	for x in args:
		ls.append(x.get_list())
	return Lst(*ls)

def at(env, n, xs):
	ls = []
	for x in args:
		ls.append(x.get_list())
	return Lst(*ls)

def wrap(env, vau_expr):
	vau = eval_(env, vau_expr)	
	f = vau.get_func()
	
	def wrapped(env, *args):		
		ps = [eval_(env, arg) for arg in args]
		return f(env, *ps)
		
	return Vau(wrapped)
	


			
			
			
	
def apply_(env, vau, args):
	f = vau.get_func()
	return f(env, *args)
	
def eval2(env, e, s):
	return eval_(eval_(env, e), eval_(env, s))

def eval_(env, x):
	print("eval: {}".format(x))
	
	#if isa(x, Lit):
	#	return Val(x.get())

	if isa(x, Val):
		return x  #env.get(x.get_val())
		
	elif isa(x, Sym):
		return env.get(x)

	elif isa(x, Lst):
		xs = x.get_list()
		if isa(xs[0], Vau):
			return apply_(env, xs[0], xs[1:])
		else:
			op = eval_(env, xs[0])
			#print ']]]',xs[0], op
			return apply_(env, op, xs[1:])
			
	else:
		assert 0, type(x)


_uid = 0
def uid(env):
	global _uid
	_uid += 1
	return Str('_u'+str(_uid))

def nil(env):
	return Nil()
	
def num(env, a):
	assert isa(a, Lit)
	return Int(int(a.get()))

def str_(env, a):
	assert isa(a, Lit)
	return Str(str(a.get()))

def nand(env,a,b):
	x = eval_(env,a)
	y = eval_(env,b)
	assert isa(x, Int)
	assert isa(y, Int)
	return Int(not(x.get() and y.get()))
	
def lt(env,a,b):
	return Int(eval_(env,a).get_val() < eval_(env,b).get_val())
	
def len_(env,a):
	x = eval_(env,a)
	assert isa(x, Seq)
	return Int(len(x.get_list()))

def eq(a,b):
	assert isa(a, Int)
	assert isa(b, Int)
	return Int(a.get_val() == b.get_val())

def read_file(env,a):
	x = eval_(env,a)
	assert isa(x, Lit)	
	return Lit(open(x.get()).read())


def if1(env,c,a):
	x = eval_(env, c)
	if x.get():
		return eval_(env, a)
	return Nil()




glob = Env(None)

def init(s, f):
	glob.set(Atm(s), Vau(f))


init('vau', vau)
init('eval', eval2)
init('wrap', wrap)
init('list', list_)

init('nil', nil)
init('def', def_)
init('do', begin)
init('if1', if1)

init('cat', concat)
init('at', at)
init('len', len_)

init('num', num)
init('str', str_)
init('nand', nand)
init('<', lt)
init('==', eq)
init('+', add)
init('-', sub)

init('uid', uid)






#init('open', open_)
init('read-file', read_file)
#init('write', write)
#init('close', close)
init('print', print_)

#init('parse', parse)





init('block', argblock)


ts = [
'''
(do
	(def quote (vau (x) env x))
	
	(def lambda
		(vau (args body) s-env
			(wrap (eval s-env (list (quote vau) args (quote d-env) body)))))
	

	(def * (lambda (x y) (do
		(def t (uid))	
		(print (list 'def t (list '* x y)))
		t
	)))

	(def + (lambda (x y) (do
		(def t (uid))	
		(print (list 'def t (list '* x y)))
		t
	)))

	(def sqrt (lambda (x) (do
		(def t (uid))	
		(print (list 'def t (list 'sqrt x)))
		t
	)))

	(sqrt (+ (* 1 1) (* 2 2)))
)
'''
]


'''
(do

	(def quote (vau (x) env x))
	
	(def lambda
		(vau (args body) s-env
			(wrap (eval s-env (list (quote vau) args (quote d-env) body)))))
	
	(print ((lambda (x y) (+ x y)) 1 2))
	
	
	(def add (block 
		(arg x)
		(arg y)
		(def z (+ x y))
		z
	))
	
	(print (add 5 6))
	
)
'''




'''
(block
	(def # 
		(vau (e) % e)
	)
	
	[1 + 2 ]
	

	(def fun
		(vau (args body) static-env
			(wrap (eval static-env (list (# vau) args (# dynamic-env) body)))))
			
			
	(print ((fun (x y) {(+ x y)}) 1 2))
)
'''



[

'''

(def lambda (args body)

(def f (vau (x y) % (+ (eval % x) (eval % y))))

(def lam
	(vau (args body) %
		(list (# vau) (eval % args) (# $) (eval % body))))
		
(print (lam (x y) (+ x y)))

(eval % args)
(eval % body)

(def f (lambda (x y) (+ x y)))



	(vau args 0

'''
,
'''
(block
	
	(#
		(def r 12)
		(def t r)

		((vau (a b) ev (print (eval ev b))) g t)
	)
		
	(def fun (vau (a b) ev (print (+ (eval ev a) (eval ev b)))))
	
	(fun 1 3)
	

	(block
		(def x 4)
		(def y 2)
		
		(print (+ x y))
	)
)
'''
]


'''

		if '.' in num_str:
			try:
				return ('FLOAT', float(num_str))
			except ValueError:
				raise ParseError("invalid float literal {}", repr(num_str))
		else:
			try:
				return ('INT', int(num_str))
			except ValueError:
				raise ParseError("invalid int literal {}", repr(num_str))
		
		assert 0
'''


def main():
	import sys	
	
	fn = sys.argv[1]
	
	src = open(fn).read()
	pt = parse(src)  
	result = eval_(glob, pt)
	
			

if __name__ == '__main__':
	main()






	
'''
class SymTab:

	def __init__(self):
		self.sym2id = {}
		self.id2sym = {}
		self.next_id = 0
			
	def get_id(self, txt):
		if txt not in self.sym2id:
			id = self.next_id
			self.next_id += 1
			self.sym2id[txt] = id
			self.id2sym[id] = txt
			
		return self.sym2id[txt]
	
	def get_name(self, id):
		return self.id2sym[id]
		
	def atomize(self, pnode):		
		typ,arg = pnode
		if typ == 'LIST':
			# arg is list of pnodes
			return Lst([self.atomize(x) for x in arg])

		elif typ == 'ATOM':
			try:
				return Val(int(arg))
			except ValueError:
				pass

			return Sym(self.get_id(arg))  #self.sym2id[arg]
			
		else:
			raise Exception('Cannot atomize: ' + root[0])
'''
