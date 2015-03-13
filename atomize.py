from data import *

class ch:
	digit = "1234567890"
	lower = "qwertyuiopasdfghjklzxcvbnm"
	upper = "QWERTYUIOPASDFGHJKLZXCVBNM"
	white = " \t\r\n"
	symbol = lower + digit + upper + "_+-*/#%$@!^&*" 

class ParseError(Exception):
	pass
	
def parse(src):
	i = 0
	
	col = 1
	row = 1
	
	def get():
		nonlocal i
		try:
			if i < len(src):
				print(src[i], end='')
				return src[i]
			return "TERMINAL"
		finally:
			i += 1
			
	def peek():
		if i < len(src):
			return src[i]
		return "TERMINAL"
	
	def accept_white():
		if peek() in ch.white:
			return ('WHITE', get())
		else:
			raise ParseError("expected '{}'".format(c))
		
	def accept_char(c):
		if peek() in c:
			return ('CHAR', get())
		else:
			raise ParseError("expected '{}'".format(c))
		
	def accept_symbol():
		cs = []
		while peek() in ch.symbol:
			cs.append(get())
				
		if not cs:
			raise ParseError("expected symbol")
		return ("ATOM", "".join(cs))

	def accept_list():
		accept_char('(')
		_,args = accept_list_body()		
		accept_char(')')
		return ("LIST", args)
		
	def optional_white():
		while peek() in ch.white:
			get()
			
		
	def accept_list_body():
		args = []
		while 1:
			#print(repr(peek()))
			if peek() in ch.white:
				accept_white()
			elif peek() in ch.symbol:
				args.append(accept_symbol())
			elif peek() in '(':
				args.append(accept_list())
			else:
				break
		return ("LISTBODY", args)
	
	try:
		# _,args = accept_list_body()
		optional_white()
		ret = accept_list()
		optional_white()
		
		if peek() != "TERMINAL":
			raise ParseError("leftover: " + str(src[i:]) + repr(peek()))
	except ParseError as e:
		print("ParseError at {}: {}".format(i, e.args[0]))
		raise
			
	print('TERMINAL')
	print()
	return ret #("LIST", args)
		


#----------------------------------------------

class Base:
	def __init__(self, args):
		self.args = args
	
class Int(Base): 
	def get_int(self): 
		return self.args
		
class Symbol(Base): 
	def get_id(self): 
		return self.args
		
class List(Base):
	def get_list(self): 
		return self.args
	

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


		
ts = [
	"alamakota", 
	"()",
	"(ala23)",
	" ( 3 op ) ",
	" ( 3 (op dfg) ) ",
]	
		
		
if __name__ == "__main__":
	for t in ts:
		print(atomize(t))
	















	
		
		
"""	
# active blocks
blocks = []




def process(src)


float_zero { 0.0f }

; template
id
nargs
 arg_name arg_type
 ...
size
 body
 





; template definition
def dist2 {

	arg r FloatPtr   ; template argument declaration
	arg x FloatPtr
	arg y FloatPtr 

	reg t Float  ; local var (allocated statically in data or stack section)
	
	mul r x x
	mul t y y
	add r r t
	
	(%for %3
		'(while 1 (block
		
		))
	)		
}


// allocated stack size is known at compile time - yes because no dynamic alloc
// no recursive functions 
// everything inlined

k { 1.0f }
l { 2.0f }
r { Float }

(dist2 r k l)      // inline




eval
	template arg1 arg2
	or
	atomic-template arg1 arg2

	
active templates
	template
		list of args
			arg
				name
				type








































emit 

: start
: zero
val u16 <u16>
val u16 ?
put u16 [@] <label> <u16>
sub u16 [@] <label> [@] <label>
sub f32 [@] <label> [@] <label>
add u16 [@] <label> [@] <label>
add f32 [@] <label> [@] <label>
mul u16 [@] <label> [@] <label>
mul f32 [@] <label> [@] <label>
div u16 [@] <label> [@] <label>
div f32 [@] <label> [@] <label>
cpy8  [@] <label> [@] <label>
cpy16 [@] <label> [@] <label>
cpy32 [@] <label> [@] <label>
jnz u16 <label> [@] <label>
cuf [@] <label> [@] <label>
cfu [@] <label> [@] <label>
mod u16 [@] <label> [@] <label>
jmp <label>
hlt

def ,x ,y
set ,x ,y
decl ,label
goto ,label
ife ,cond ,ontrue ,onfalse
write ,num
read 
+ ,x ,y
- ,x ,y
* ,x ,y
// ,x ,y
% ,x ,y
== ,x ,y
<= ,x ,y
<< ,x ,y
>> ,x ,y
!&
nand


"""
