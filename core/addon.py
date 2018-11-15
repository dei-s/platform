class Addon:
	def __init__(self, name, handle):
		if name.startswith('addons.'):
			name = name[7:]
		self.name = name
		self.handle = handle
