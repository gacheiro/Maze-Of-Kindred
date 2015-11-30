class Animation ():

	def __init__ (self, duration, frames):
		
		if not isinstance(frames, (list, tuple)):
			frames = [frames]
		
		self.frames = frames
		self.len = len(frames)
		self.state = 0
		self.duration = duration
		self.time_passed = 0
		
		self.playing = False
		self.loop = False
		
		self.frame_time = self.duration / self.len
		
	def play (self, loop=False):
	
		self.time_passed = 0
		self.state = 0
		
		self.playing = True
		self.loop = loop
	
	def update (self, time_passed):
	
		if not self.playing:
			return
			
		elif self.is_complete():
			return
		
		self.time_passed += time_passed
		self.state = int(self.time_passed / self.frame_time) % self.len
		
	def get_image (self):
	
		return self.frames[self.state]
		
	def is_complete (self):

		_r = False
		
		if self.loop:
			pass

		elif self.state == self.len - 1:
			self.playing = False
			_r = True
			
		return _r
