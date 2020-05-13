
from collections import OrderedDict
import time
cache = OrderedDict() #remove key/value and re-add when cache hit


# def clock(func):
#    def clocked(*args):
#        t0 = time.perf_counter()
#        result = func(*args)
#        elapsed = time.perf_counter() - t0
#        name = func.__name__
#        arg_str = ', '.join(repr(arg) for arg in args)
#        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
#        return result
#    return clocked

# def lru_cache(func):
# 	def cache_inner(*args):
# 		t_start = time.perf_counter()
# 		time_print = ""
# 		if (args[0] in cache): #cache hit
# 			temp = cache[args[0]]
# 			del cache[args[0]]
# 			#reorder cache to LRU
# 			cache[args[0]] = temp
# 			print("[cache-hit]", func.__name__ + "(" + str(args[0]) + ")", "->", temp)
# 		else:
# 			#cache miss
# 			t_diff = time.perf_counter() - t_start

def lru_cache(size):
	def cache_inner(func):
		t_start = time.perf_counter()
		def cache_inner_inner(*args):
			time_print = ""
			result = 0
			if (args[0] in cache): #cache hit
				temp = cache[args[0]]
				del cache[args[0]]
				#reorder cache to LRU
				cache[args[0]] = temp
				print("[cache-hit]", func.__name__ + "(" + str(args[0]) + ")", "->", temp)
				result = temp
			else:
				#cache miss
				t_diff = time.perf_counter() - t_start
				result = func(args[0]) #expensive part, you recall function for full computation cost since you cache missed
				#if cache full, remove LRU add new item
				if len(cache) >= size:
					del cache[list(cache.keys())[0]]
				cache[args[0]] = result
				func_sig = func.__name__ + "(" + str(args[0]) + ")"
				print('[%0.8fs] %s -> %r' % (t_diff, func_sig, result))

			return result

		return cache_inner_inner

	return cache_inner





class Cache:

	def __init__(self, maxLen):
		self.q = []
		self.max = maxLen

		def add(self, data):
			self.q.append(data)

		def canAddElem(self):
			if len(q) < self.max and data not in q:
				return True
			return false
		def hasElem(self, elem):
			if elem in q:
				return True
			return False

		def reorder(idx):
			temp = q[idx]
			del q[idx]
			q.append(temp)
