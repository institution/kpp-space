# coding: utf-8
import sys
from data import Error
from reader import Reader

class PreprocError(Error):
	pass


def preproc(r, debug=0):
	""" 
	* remove end line comments
	* convert indentation to braces
	* insert braces on "inline indents" ('\' notation)
	
	Operates on character level
	
	r -- reader
	yield -- characters
	"""
	
	if debug:
		auto_open = '['
		auto_close = ']'
	else:
		auto_open = '('
		auto_close = ')'
		
	stack = []
	ci = 0       # current indentation
	first_on_line = 1
	produced = []
	
	def produce(x):
		produced.append(x)
	
	def close_automatic_braces():
		while stack:
			t,ti = stack[-1]
			if t == '[':
				if ti >= ci:
					produce(auto_close)
					stack.pop()
				else:
					break
			else:
				break
			
	def close_manual_brace():
		if not stack:
			raise PreprocError('encountered unmatched closing brace')
		t,ti = stack[-1]
		assert t == '('
		assert ti <= ci
		produce(')')
		stack.pop()
			
	def open_automatic_brace():
		produce(auto_open)
		stack.append(('[',ci))
	
	def open_brace():
		produce('(')
		stack.append(('(',ci))
	
	
	while 1:
		if r.peek() == '#':
			r.get()
			while r.peek() != '\n':
				r.get()
		
		elif r.peek() == '\\':
			# inline indentation
			if first_on_line:
				first_on_line = 0
				
			open_automatic_brace()
			r.get()
			
		elif r.peek() == '\t':
			if first_on_line == 0:
				raise PreprocError('tab inside line body')
			ci += 1			
			r.get()
			
			produce('\t')
			
		elif r.peek() == '\n':		
			r.get()
			first_on_line = 1
			ci = 0
			
			produce('\n')
			
			
		
		elif r.peek() == ' ':
			if first_on_line:
				raise PreprocError('space at the beginning of the line {}, pos {}', r.row, r.col)
			else:
				produce(' ')
				r.get()
				
		elif r.peek() == '(':
			if first_on_line:
				close_automatic_braces()
				first_on_line = 0
				
			open_brace()				
			r.get()
		
		
		elif r.peek() == ')':
			close_automatic_braces()
			close_manual_brace()
			
			r.get()
			
			if first_on_line:
				first_on_line = 0
				
				
		elif r.peek() == 'TERMINAL':
			close_automatic_braces()
			if stack:
				raise PreprocError('there are opened braces still left at end of the file')
			
			break
		
		else:
			if first_on_line:				
				close_automatic_braces()				
				first_on_line = 0				
				open_automatic_brace()
							
			produce(r.get())
								
		for p in produced:
			yield p			
		produced = []
		
		
	for p in produced:
		yield p			
	produced = []


		
def test(src, res):
	if __name__ == '__main__':
		print '==================================='
		print src
		print '-----------------------------------'
		for x in preproc(Reader(src), debug=True):
			sys.stdout.write(x)
		print
			
src = """
(aaa bbb
	ccc
	ddd
		eee
		(fff ggg)
		fff ggg
)
"""
res = """
(aaa bbb[ccc][ddd[eee](fff ggg)[fff ggg]])
"""
test(src, res)

src = """
aaa
	bbb
		ccc
	ddd
	eee

"""
res = """
[aaa[bbb[ccc]][ddd][eee]]
"""
test(src, res)

src = """
(aaa bbb
	ccc (ddd
	) eee
)
"""
res = """
(aaa bbb[ccc (ddd) eee])
"""
test(src, res)

src = r"""
aaa \bbb
	xxx
	yyy

"""
res = """
[aaa [bbb[xxx][yyy]]]
"""
test(src, res)

src = r"""
\bbb
	xxx
	yyy

"""
res = """
[bbb[xxx][yyy]]
"""
test(src, res)

