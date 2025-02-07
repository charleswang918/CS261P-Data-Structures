# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List, Optional

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[Optional[int]]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		eviction = 0
		table_idx = 0
		while eviction <= self.CYCLE_THRESHOLD:
			hash_idx = self.hash_func(key, table_idx)
			if self.tables[table_idx][hash_idx] is None:
				self.tables[table_idx][hash_idx] = key
				return True
			else:
				collision_val = self.tables[table_idx][hash_idx]
				self.tables[table_idx][hash_idx] = key
				key = collision_val
				eviction += 1
				table_idx = 1 - table_idx
		return False



	def lookup(self, key: int) -> bool:
		# TODO
		for i in range(len(self.tables)):
			hash_idx = self.hash_func(key, i)
			if self.tables[i][hash_idx] == key:
				return True
		return False
		

	def delete(self, key: int) -> None:
		# TODO
		for i in range(len(self.tables)):
			hash_idx = self.hash_func(key, i)
			if self.tables[i][hash_idx] == key:
				self.tables[i][hash_idx] = None
				break

	def rehash(self, new_table_size: int) -> None:
		self.__num_rehashes += 1; self.table_size = new_table_size  # do not modify this line
		# TODO
		old_table = self.tables
		new_table = [[None]*new_table_size for _ in range(2)]
		self.tables = new_table
		for i in range(len(old_table)):
			for j in range(len(old_table[i])):
				if old_table[i][j] is not None:
					key = old_table[i][j]
					self.insert(key)


# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define

