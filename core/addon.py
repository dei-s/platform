class Addon:
	def __init__(self, name, handleHttp, handleMessage):
		if name.startswith('addons.'):
			name = name[7:]
		self.name = name
		self.handleHttp = handleHttp
		self.handleMessage = handleMessage
