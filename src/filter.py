import time
import heapq as hq
import threading
import random

class mosc_buffer(object):
	def __init__(self):
		self.created = time.time()
		super(mosc_buffer, self).__init__()
		self.total = 15
		self.data, self.calls, self.sms, self.emergencies = [], [], [], []
		self.past_num_data, self.past_num_calls, self.past_num_sms, self.past_num_emergencies = 0, 0, 0, 0
		self.max_data = self.total * 0.1
		self.max_call = self.total * 0.3
		self.max_sms = self.total * 0.4
		self.max_emergencies = self.total * 0.2
		threading.Timer(5.0, self.refresh_buffer).start()
		threading.Timer(1.0, self.expire).start()
		self.total_ecalls, self.total_calls, self.total_sms, self.total_data = 0, 0, 0, 0
		self.served_ecalls, self.served_calls, self.served_sms, self.served_data = 0, 0, 0, 0

	def add(self, packet_type):
		self.reassign_buffers()
		if self.filter(packet_type):
			if packet_type == "data":
				self.served_data += 1
				self.data.append(time.time())
				return True
			elif packet_type == "call":
				self.served_calls += 1
				self.calls.append(time.time())
				return True
			elif packet_type == "sms":
				self.served_sms += 1
				self.sms.append(time.time())
				return True
			elif packet_type == "ecall":
				self.served_ecalls += 1
				self.emergencies.append(time.time())
				return True
		return False

	def filter(self, packet_type):
		prob = 0
		if packet_type == "data":
			self.total_data += 1
			if self.data == None:
				return False
			prob = (self.max_data - len(self.data)) / self.past_num_data if self.past_num_data else 1
		elif packet_type == "call":
			self.total_calls += 1
			if self.calls == None:
				return False
			prob = (self.max_calls - len(self.calls)) / self.past_num_calls if self.past_num_calls else 1
		elif packet_type == "sms":
			self.total_sms += 1
			if self.sms == None:
				return False
			prob = (self.max_sms - len(self.sms)) / self.past_num_sms if self.past_num_sms else 1
		elif packet_type == "ecall":
			self.total_ecalls += 1
			prob = (self.max_emergencies - len(self.emergencies)) / self.past_num_emergencies if self.past_num_emergencies else 1
		if prob > 1:
			return True
		return random.random() < prob

	def refresh_buffer(self):
		self.past_num_data = len(self.data)
		self.past_num_calls = len(self.calls)
		self.past_num_sms = len(self.sms)
		self.past_num_emergencies = len(self.emergencies)

	def reassign_buffers(self):
		if len(self.calls) >= self.max_call:
			self.max_call += self.max_data
			self.max_data = 0
		if len(self.sms) >= self.max_sms:
			self.max_sms += self.max_call
			self.max_call = 0
		if len(self.emergencies) >= self.max_emergencies:
			self.max_emergencies += self.max_sms
			self.max_sms = 0
		if len(self.calls) <= self.max_call / 2 and self.max_data == 0:
			self.max_data = self.max_call / 4
			self.max_call -= self.max_data
		if len(self.sms) <= self.max_sms / 2 and self.max_call == 0:
			self.max_call = self.max_sms / 4
			self.max_sms -= self.max_call
		if len(self.emergencies) <= self.max_emergencies / 2 and self.max_sms == 0:
			self.max_sms = self.max_emergencies / 4
			self.max_emergencies -= self.max_sms

	def expire(self):
		self.data = [x for x in self.data if not self.expired_data(x)]
		self.calls = [x for x in self.calls if not self.expired_calls(x)]
		self.sms = [x for x in self.sms if not self.expired_sms(x)]
		self.emergencies = [x for x in self.emergencies if not self.expired_emergencies(x)]

	def expired_data(x):
		return time.time() - x[0] >= 10

	def expired_calls(x):
		return time.time() - x[0] >= 20

	def expired_sms(x):
		return time.time() - x[0] >= 2

	def expired_emergencies(x):
		return time.time() - x[0] >= 20

	def num_received_ecalls(self):
		return self.total_ecalls

	def num_served_ecalls(self):
		return self.served_ecalls

	def num_received_calls(self):
		return self.total_calls

	def num_served_calls(self):
		return self.served_calls

	def num_received_sms(self):
		return self.total_sms

	def num_served_sms(self):
		return self.served_sms

	def num_received_data(self):
		return self.total_data

	def num_served_data(self):
		return self.served_data
