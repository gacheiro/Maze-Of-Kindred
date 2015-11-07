class animation ():

	def __init__ (self, images):
		
		self.images = images
		self.len = len(images)
		self.state = 0
		self.time_total = 1
		self.time_passed = 0
		
		self.playing = False
		self.complete = False
		
		self.delay_per_frame = self.time_total / self.len	
		
	def play (self, time_total):
	
		self.time_total = time_total
		self.time_passed = 0
		self.state = 0
		self.playing = True
		
		self.delay_per_frame = time_total / self.len	
	
	def update (self, time_passed):
	
		if self.playing == False or self.time_passed >= self.time_total:
			return
		
		self.time_passed += time_passed
			
		self.state = self.time_passed / self.delay_per_frame - 1
		
		self.is_complete()
		
	def get_image (self):
	
		self.state = self.state % self.len
		return self.images[self.state]
		
	def is_complete (self):

		self.complete = False
		
		if self.state == self.len - 1:
		
			self.complete = True
			self.playing = False

		return self.complete
		
