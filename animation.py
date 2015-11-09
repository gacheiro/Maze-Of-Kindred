class animation ():

	def __init__ (self, images):
		
		assert(len(images) > 0)
		
		self.images = images
		self.len = len(images)
		self.state = 0
		self.time_total = 0
		self.time_passed = 0
		
		self.playing = False
		self.loop = False
		
		self.frame_time = 1 # to avoid 0/0	
		
	def play (self, time_total, loop=False):
	
		self.time_total = time_total
		self.time_passed = 0
		self.state = 0
		
		self.playing = True
		self.loop = loop
		
		self.frame_time = time_total / self.len
	
	def update (self, time_passed):
	
		if not self.playing:
			return
			
		elif self.is_complete():
			return
		
		self.time_passed += time_passed
		self.state = int(self.time_passed / self.frame_time) % self.len
		
	def get_image (self):
	
		return self.images[self.state]
		
	def is_complete (self):

		_r = False
		
		if self.loop:
			pass

		elif self.state == self.len - 1:
			self.playing = False
			_r = True
			
		return _r
