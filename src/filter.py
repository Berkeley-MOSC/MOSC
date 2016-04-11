import time
import heapq as hq
import threading
import random

class mosc_buffer(object):
	def __init__(self, arg):
		self.created = time.time()
		super(mosc_buffer, self).__init__()
		self.total = 1000
		self.data, self.calls, self.sms, self.emergencies = [], [], [], []
		self.past_num_data, self.past_num_calls, self.past_num_sms, self.past_num_emergencies = 0, 0, 0, 0
		self.max_data = self.total * 0.1
		self.max_call = self.total * 0.3
		self.max_sms = self.total * 0.4
		self.max_emergencies = self.total * 0.2
		threading.Timer(5.0, refresh_buffer).start()

	def add(self, packet):
		if self.filter(packet):
			self.buffer.append(packet)

	def filter(self, packet):
		prob = 0
		if packet == "data":
			# Drop because the data buffer is len 0 since allocated space up the chain
			if self.data == None:
				return False
			else:
				prob = (self.max_data - len(self.data)) / self.past_num_data
		elif packet == "call":
			if self.calls == None:
				return False
			else:
				prob = (self.max_calls - len(self.calls)) / self.past_num_calls
		elif packet == "sms":
			if self.sms == None:
				return False
			else:
				prob = (self.max_sms - len(self.sms)) / self.past_num_sms
		elif packet == "emergencies":
			prob = (self.max_emergencies - len(self.emergencies)) / self.past_num_emergencies
		if prob > 1:
			return True
		else:
			return random.random() < prob

	def refresh_buffer(self):
		self.past_num_data, self.past_num_calls, self.past_num_sms, self.past_num_emergencies = len(self.data), len(self.calls), len(self.sms), len(self.emergencies)

	def reassign_buffers(self):
