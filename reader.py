
class Reader:
	def __init__(self, src):
		self.osrc = unicode(src)
		self.src = unicode(src)
		self.i = 0
		self.col = 1
		self.row = 1
	
	def get(self):
		try:
			if self.i < len(self.src):
				c = self.src[self.i]
				# print(c, end='')
				if c == '\n':
					self.row += 1
					self.col = 1
				else:
					self.col += 1
					
				return c
								
			return "TERMINAL"
			
		finally:
			self.i += 1
	
	def peek(self):
		if self.i < len(self.src):
			c = self.src[self.i]
			return c
			
		return "TERMINAL"
		
