from atomize import parse, SymTab,Symbol, Int, List
import types
from data import *


symtab = SymTab()
Sym.symtab = symtab

# int -> list|int
# int -> [LAMBDA ...] for user defined functions
# int -> function -- for buildin functions
deftab = {}

def isa(x,t):
	return type(x) == t

	
# -----------------------------





def print_(env, a):
	print("OUTPUT: {}".format(eval_(env, a)))
		
def block(env, *args):
	loc = Env(env)
	
	r = Nil()
	for a in args:
		r = eval_(loc, a)
		
	return r

def def_(env, a, b):
	env.set(a, eval_(env, b))
	return Nil()

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
		assert len(self.s_args.get_list()) == len(args)
		
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
	return Lst([eval_(env, x) for x in args])

def quote(env, arg):
	return arg

def concat(env, *args):
	ls = []
	for x in args:
		ls.append(x.get_list())
	return Lst(ls)

def at(env, n, xs):
	ls = []
	for x in args:
		ls.append(x.get_list())
	return Lst(ls)

def wrap(env, vau):
	f = vau.get_func()
	def inner(env, *args):		
		ps = [eval_(env, arg) for arg in args]
		return f(*ps)
		
	return Vau(wrapped)

	
def apply_(env, vau, args):
	f = vau.get_func()
	return f(env, *args)
	
def eval2(env, e, s):
	return eval_(eval_(env, e), eval_(env, s))

def eval_(env, x):
	print("eval: {}".format(x))
	if isa(x, Lit):
		return Val(x.get_val())

	elif isa(x, Val):
		return x  #env.get(x.get_val())
		
	elif isa(x, Sym):
		return env.get(x)

	elif isa(x, Lst):
		xs = x.get_list()
		if isa(xs[0], Vau):
			return apply_(env, xs[0], xs[1:])
		else:
			op = eval_(env, xs[0])
			return apply_(env, op, xs[1:])
			
	else:
		assert 0, type(x)
		


glob = Env(None)

def init(s, f):
	glob.set(Sym(symtab.get_id(s)), Vau(f))
	
init('def', def_)
init('block', block)
init('concat', concat)
init('print', print_)
init('+', add)
init('-', sub)
init('vau', vau)
init('eval', eval2)
init('list*', list_)
init('#', quote)


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


ts = [
'''
(block
	(def lam
		(vau (args body) %
			(block			
				(def eargs (map eval args))
				(list* (# vau) args (# $) body)
				
				
			
	(print (lam (x y) (+ x y)))
)
'''
]

[
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




def main():
	
	for src in ts:
		print("--------------------------------------")
		
		# parse tree <- src
		pt = parse(src)  

		# symbol tree <- parse tree
		st = symtab.atomize(pt)
		
		#print('program = ', pp(st, symtab, deftab), sep='')
		
		try:
			print(eval_(glob, st))
		finally:
			print(glob.tab)
		
		

main()



