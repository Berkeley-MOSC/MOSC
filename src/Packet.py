allowed_types = ["data", "call", "emergency", "sms"]

class Packet:
	self.type = ""
	def __init__(self, str_type):
		if str_type in allowed_types:
			self.type = str_type
		else:
			raise ValueError("Packet is not a valid type.")