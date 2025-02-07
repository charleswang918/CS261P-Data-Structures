# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash24:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.bucket_size = 4
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.table = [None]*self.table_size

	def get_rand_bucket_index(self, bucket_idx: int) -> int:
		# you must use this function when you need to evict a random key from a bucket. this function
		# randomly chooses an index from a given cell index. this ensures that the random
		# index chosen by your code and our test script match.
		#
		# for example, if you need to remove a random element from the bucket at table index 5,
		# you will call get_rand_bucket_index(5) to determine which key from that bucket to evict, i.e. if get_random_bucket_index(5) returns 2, you
		# will evict the key at index 2 in that bucket.
		rand.seed(int(str(bucket_idx)))
		return rand.randint(0, self.bucket_size-1)

	def hash_func(self, key: int, func_id: int) -> int:
		# access h0 via func_id=0, access h1 via func_id=1
		key = int(str(key) + str(self.__num_rehashes) + str(func_id))
		rand.seed(key)
		result = rand.randint(0, self.table_size-1)
		return result

	def get_table_contents(self) -> List[Optional[List[int]]]:
		# the buckets should be implemented as lists. Table cells with no elements should still have None entries.
		return self.table

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		eviction = 0
		while eviction <= self.CYCLE_THRESHOLD:
			for idx in range(2):
				hash_idx = self.hash_func(key, idx)
				if self.table[hash_idx] is None:
					self.table[hash_idx] = [key]
					return True
				elif len(self.table[hash_idx]) < self.bucket_size:
					self.table[hash_idx].append(key)
					return True
				else:
					collision_idx = self.get_rand_bucket_index(hash_idx)
					collision_val = self.table[hash_idx][collision_idx]
					self.table[hash_idx][collision_idx] = key
					key = collision_val
			eviction += 1
		return False

	def lookup(self, key: int) -> bool:
		# TODO
		for i in range(2):
			idx = self.hash_func(key, i)
			bucket = self.table[idx]
			if bucket is not None and key in bucket:
				return True
		return False
		

	def delete(self, key: int) -> None:
		# TODO
		for i in range(2):
			idx = self.hash_func(key, i)
			bucket = self.table[idx]

			if bucket is not None and key in bucket:
				bucket.remove(key)
				if len(bucket) == 0:
					self.table[idx] = None
				break

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line
		# TODO
		old_table = self.table
		new_table = [None] * new_table_size
		self.table = new_table
		for bucket in old_table:
			if bucket is not None:
				for ele in bucket:
					self.insert(ele)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define


