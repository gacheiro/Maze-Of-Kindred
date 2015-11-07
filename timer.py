class timer ():

	def __init__ (self, time):
	
		self.time = time
		self.time_passed = 0
	
	def update (self, time_passed):
	
		self.time_passed += time_passed
	
	def reset (self):
	
		self.time_passed = 0
	
	def is_complete (self):
	
		return self.time_passed >= self.time

