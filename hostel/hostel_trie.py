import pickle
from hostel.models import Hostel

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class HostelTrie:
    def __init__(self):
        self.trie_root = TrieNode()
        self.hash_table = {}

    def preprocess_name(self, hostel_name):
        common_prefixes = ["girls", "boys", "hostel"]  # Only remove "girls" and "boys"
        words = hostel_name.lower().split()
        filtered_words = [word for word in words if word not in common_prefixes]
        return " ".join(filtered_words)

    def build_from_array(self, hostel_names):
        for hostel_name in hostel_names:
            preprocessed_name = self.preprocess_name(hostel_name)
            self.insert_hostel(preprocessed_name, hostel_name)
            print(f"Processed: {hostel_name}, Hash Table: {self.hash_table}")

    def insert_hostel(self, hostel_name_lower, original_hostel_name):
        current_node = self.trie_root

        for char in hostel_name_lower:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]

        current_node.is_end_of_word = True
        if hostel_name_lower not in self.hash_table:
            self.hash_table[hostel_name_lower] = {'original_hostels': set()}
        self.hash_table[hostel_name_lower]['original_hostels'].add(original_hostel_name)

    def search(self, query):
        exact_matches = set()
        partial_matches = set()
        current_node = self.trie_root
        matched_prefix = ""
        
       
        for char in query.lower():
            if char in current_node.children:
                current_node = current_node.children[char]
                matched_prefix += char
                if current_node.is_end_of_word:
                    exact_matches.add(matched_prefix)
            else:
                break
        print("Hash Table:", self.hash_table)

        # Check for partial matches in children nodes
        
        if len(matched_prefix)>= 4:
            for child_char, child_node in current_node.children.items():
                self._get_all_hostels_from_node(child_char, child_node, matched_prefix, partial_matches)

        print("Exact Matches:", exact_matches)
        print("Partial Matches:", partial_matches)
        print("Hash Table:", self.hash_table)

        # If there is at least one exact match, return the results
        if exact_matches or partial_matches:
            # Convert sets to lists and sort based on exact matches
            exact_sorted = sorted(list(exact_matches), key=lambda x: x == query.lower(), reverse=True)
            partial_sorted = sorted(list(partial_matches), key=lambda x: len(x))

            # Flatten the lists of hostels
            exact_results = [hostel for sublist in exact_sorted for hostel in self.hash_table[sublist]['original_hostels']]
            partial_results = [hostel for sublist in partial_sorted for hostel in self.hash_table[sublist]['original_hostels']]
            print(partial_results)

            return exact_results + partial_results
        else:
            return []

    def _get_all_hostels_from_node(self, char, node, current_prefix, results):
        if node.is_end_of_word or not node.children:
            results.add(current_prefix + char)

        for child_char, child_node in node.children.items():
            self._get_all_hostels_from_node(child_char, child_node, current_prefix + char, results)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.trie_root, file)

    @classmethod
    def load_from_file(cls, filename):
        trie = cls()
        with open(filename, 'rb') as file:
            trie.trie_root = pickle.load(file)
        return trie


hostel_queryset = Hostel.objects.all()
hostel_names = [hostel.name for hostel in hostel_queryset]
hostel_trie = HostelTrie()
hostel_trie.build_from_array(hostel_names)

# Save the trie to a file
hostel_trie.save_to_file('hostel_trie.pkl')
