# coding: utf-8
import sys
from data import Lit, Seq, Atm, Error
from reader import Reader
from preproc import preproc

class ch:
	digit = "1234567890"
	lower = "qwertyuiopasdfghjklzxcvbnm"
	upper = "QWERTYUIOPASDFGHJKLZXCVBNM"
	oper = "=<>*/+-&^|%!.@$:~_?"
	white = " \t\n"
	reserved = ",;'`"
	
	open_str = '"'
	close_str = '"'
		
	open_num = digit
	body_num = open_num + '.+-'
	
	open_sym = lower + upper + oper
	body_sym = open_sym + digit

	comment = '#'
	escape_char = '\\'
	

class ParseError(Error):
	pass
		
	
	
def print_error(f):
	try:
		return f()
	except Exception as e:
		print str(e)
	
	
	
	
def accept(r):
	while r.peek() in ch.white:
		r.get()
	
def exact_char(r, c):
	"""
	>>> print exact_char(Reader("2"), "2")
	"2"
	>>> print_error(lambda: exact_char(Reader("2"), "3"))
	expected '3', got '2'
	"""
	if r.peek() == c:
		return Lit(r.get())
	else:
		raise ParseError("expected {}, got {}", repr(c), repr(r.peek()))
	
def accept_string(r):
	"""
	>>> print accept_string(Reader('"aaa"'))
	(str "aaa")
	>>> print accept_string(Reader('""'))
	(str "")
	"""
	exact_char(r, ch.open_str)
	cs = []
	while r.peek() not in ch.close_str:
		cs.append(r.get())
	exact_char(r, ch.close_str)
	accept(r)
	return Seq(Atm("str"), Lit(''.join(cs)))


def accept_number(r):
	"""
	>>> print accept_number(Reader('0-123.0'))
	(num "0-123.0")
	"""
	
	if r.peek() not in ch.open_num:
		raise ParseError("number can not begin with {}", repr(r.peek()))
		
	cs = [r.get()]
	while r.peek() in ch.body_num:
		cs.append(r.get())
	
	accept(r)
	
	return Seq(
		Atm('num'),
		Lit(''.join(cs)),
	)

def accept_symbol(r):
	"""
	>>> print accept_symbol(Reader('<-2-<'))
	<-2-<
	"""
	if r.peek() not in ch.open_sym:
		raise ParseError("symbol cannot being with {}", repr(r.peek()))
		
	cs = [r.get()]
	while r.peek() in ch.body_sym:
		cs.append(r.get())
		
	accept(r)
	return Atm("".join(cs))

def accept_char(r, c):
	"""
	>>> print accept_char(Reader("2"), "2")
	"2"
	>>> print_error(lambda: accept_char(Reader("2"), "3"))
	expected '3', got '2'
	"""
	x = exact_char(r, c)
	accept(r)
	return x
	
def accept_round(r):
	"""
	>>> print accept_round(Reader("(x ((y) z))"))
	(x ((y) z))
	"""	
	args = []
	accept_char(r, '(')		
	while r.peek() != ')':
		args.append(accept_expr(r))
	accept_char(r, ')')
	return Seq(*args)

def accept_quoted_expr(r):
	"""
	>>> print accept_quoted_expr(Reader("'x"))
	(quote x)
	"""
	accept_char(r, "'")
	return Seq(Atm('quote'), accept_expr(r))

def accept_expr(r):
	"""
	>>> print accept_expr(Reader("abc"))
	abc
	"""		
	if r.peek() in '(':
		return accept_round(r)
	elif r.peek() in ch.open_str:
		return accept_string(r)
	elif r.peek() in ch.open_num:
		return accept_number(r)
	elif r.peek() in ch.open_sym:
		return accept_symbol(r)
	elif r.peek() in "'":
		return accept_quoted_expr(r)		
	else:
		raise ParseError('expected expression but expression cannot begin with {}', repr(r.peek()))



def parse(src):
	try:
		print src
		psrc = ''.join(preproc(Reader(src)))
		
		print psrc
		r = Reader(psrc)
		
		
		
		
		accept(r)
		ret = accept_expr(r)
		
		if r.peek() != "TERMINAL":
			raise ParseError("leftover: {} {}", str(src[r.i:]), repr(r.peek()))
	
		return ret
		
	except ParseError as e:
		lines = src.split('\n')
		line = lines[r.row-1]
		print(line.replace('\t', '    '))
		print(' '*get_width(line[:r.col-1]) + '^--here!')
		print("Error on line {}, position {}, character {}: {}".format(r.row, r.col, repr(r.peek()), str(e)))
		sys.exit(1)


def get_width(xs):
	return xs.count('\t') * 3 + len(xs)



		





		
if __name__ == "__main__":
	ts = [
		'( (line1) \n(line2) )',
		'(\n) ',
		'( (aaa#e1)\nbbb) )',
		"alamakota", 
		"()",
		"(ala23)",
		"(  aaa  )  ",
		"(  ) ",
		'"alamakota"',
		'(while (< i 5) (print "i = " i))'
		
	]	

	for t in ts:
		
		print(parse(t))
	


