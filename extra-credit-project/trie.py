# explanations for member functions are provided in requirements.py
# each file that uses a skip list should import it from this file.

from typing import List, Dict

from typing import List

class TrieNode:
    def __init__(self, value=""):
        self.value = value  # Store multiple characters for compression
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self, is_compressed: bool):
        self.root = TrieNode()
        self.is_compressed = is_compressed

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end_of_word = True

    def compress(self, node=None):
        if node is None:
            node = self.root
        for char, child in list(node.children.items()):
            if len(child.children) == 1 and not child.is_end_of_word:
                # Merge with the only child
                next_node = next(iter(child.children.values()))
                merged_value = child.value + next_node.value
                node.children[char] = TrieNode(merged_value)
                node.children[char].children = next_node.children
                node.children[char].is_end_of_word = next_node.is_end_of_word
                self.compress(node)  # Recursive call to compress further if possible
            else:
                self.compress(child)

    def construct_trie_from_text(self, keys: list[str]) -> None:
        for key in keys:
            self.insert(key)
        if self.is_compressed:
            self.compress()

    def construct_suffix_tree_from_text(self, keys: list[str]) -> None:
        for key in keys:
            for i in range(len(key)):
                suffix = key[i:]
                self.insert(suffix)
        if self.is_compressed:
            self.compress()

    def search_and_get_depth(self, word: str) -> int:
        node = self.root
        depth = 0
        i = 0
        while i < len(word):
            if word[i] in node.children:
                child = node.children[word[i]]
                # Check if the remaining word starts with the child's value
                if word.startswith(child.value, i):
                    i += len(child.value)
                    depth += 1
                    node = child
                else:
                    return -1  # Partial match failure
            else:
                return -1  # No match found
        return depth if node.is_end_of_word else -1

# Assuming Trie is initialized with is_compressed=True and constructed using construct_trie_from_text or construct_suffix_tree_from_text


# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
