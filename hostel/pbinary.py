# HostelPricingBinaryTree.py

from math import radians, sin, cos, sqrt, atan2
from .models import Hostel  # Import your Hostel model

class HostelNode:
    def __init__(self, hostel):
        self.hostel = hostel
        self.left = None
        self.right = None



class HostelPricingBinaryTree:
    def __init__(self):
        self.root = None

    def insert_from_database(self):
        hostels = Hostel.objects.all()
        for hostel in hostels:
            self.insert_by_price(hostel)

    def insert_by_price(self, new_hostel):
        self.root = self._insert_by_price_recursive(new_hostel, self.root)

    def _insert_by_price_recursive(self, new_hostel, current_node):
        if current_node is None:
            return HostelNode(new_hostel)

        # Compare prices and insert accordingly
        if new_hostel.pricing < current_node.hostel.pricing:
            current_node.left = self._insert_by_price_recursive(new_hostel, current_node.left)
        else:
            current_node.right = self._insert_by_price_recursive(new_hostel, current_node.right)

        return current_node

    def get_sorted_hostels_by_price(self):
        sorted_hostels = []
        self._inorder_traversal_by_price(self.root, sorted_hostels)
        for hostel_node in sorted_hostels:
            hostel = hostel_node['hostel']
            price = hostel_node['instance']
            print(f"Hostel Name: {hostel.name}")
            print(f"Hostel Price: {hostel.pricing}")
            # ... (print other details as needed)
            print("-" * 20)  # Separator between hostels

        return sorted_hostels

    def _inorder_traversal_by_price(self, node, result):
        if node:
            self._inorder_traversal_by_price(node.left, result)
            x = "Rs." + str(round(node.hostel.pricing,0))+ "/ per month"
            result.append({'hostel': node.hostel, 'instance': x})
            self._inorder_traversal_by_price(node.right, result)

# Example usage
tree = HostelPricingBinaryTree()
tree.insert_from_database()
sorted_pricing = tree.get_sorted_hostels_by_price()
