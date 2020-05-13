import pymmh3
import math


class BloomFilter:

	def __init__(self, num_keys, fp):

		self.false_probability = fp
		self.size = self.calculate_size(num_keys, fp)
		self.num_hashes = self.calculate_hash_count(self.size, num_keys)
		self.filter = [0 for _ in range(self.size)]

	def calculate_size(self, num_keys, fp):
		return int(-(num_keys * math.log(fp))/(math.log(2)**2))

	def calculate_hash_count(self, size, num_keys):
		return int((size/num_keys) * math.log(2))

	def add(self, item):
		for i in range(self.num_hashes):
			hash_idx = pymmh3.hash(item,i) % self.size
			self.filter[hash_idx] = 1

	def is_member(self, item):
		for i in range(self.num_hashes):
			hash_idx = pymmh3.hash(item,i) % self.size
			if self.filter[hash_idx] == 0:
				return False
		return True
