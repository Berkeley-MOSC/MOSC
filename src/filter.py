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
		self.reassign_buffers()
		if self.filter(packet):
			if packet.type == "data":
				self.data.append(packet)
			elif packet.type == "call":
				self.calls.append(packet)
			elif packet.type == "sms":
				self.sms.append(packet)
			elif packet.type == "emergencies":
				self.emergencies.append(packet)

	def filter(self, packet):
		prob = 0
		if packet.type == "data":
			if self.data == None:
				return False
			prob = (self.max_data - len(self.data)) / self.past_num_data
		elif packet.type == "call":
			if self.calls == None:
				return False
			prob = (self.max_calls - len(self.calls)) / self.past_num_calls
		elif packet.type == "sms":
			if self.sms == None:
				return False
			prob = (self.max_sms - len(self.sms)) / self.past_num_sms
		elif packet.type == "emergencies":
			prob = (self.max_emergencies - len(self.emergencies)) / self.past_num_emergencies
		if prob > 1:
			return True
		return random.random() < prob

	def refresh_buffer(self):
		self.past_num_data, self.past_num_calls, self.past_num_sms, self.past_num_emergencies = len(self.data), len(self.calls), len(self.sms), len(self.emergencies)

	def reassign_buffers(self):
		pass
