
from math import radians, sin, cos, sqrt, atan2
from .models import Hostel

class HostelNode:
    def __init__(self, hostel):
        self.hostel = hostel
        self.left = None
        self.right = None

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers (you can change this if you want distance in miles)
    radius = 6371

    distance = radius * c
    return distance

class HostelBinaryTree:
    def __init__(self):
        self.root = None
        self.user_location = {'latitude': 27.6828, 'longitude': 85.323}  # Hardcoded user location

    def insert_from_database(self):
        hostels = Hostel.objects.all()
        for hostel in hostels:
            self.root = self._insert_recursive(hostel, self.root)

    def _insert_recursive(self, new_hostel, current_node):
        if current_node is None:
            return HostelNode(new_hostel)

        # Calculate distances from the hardcoded user location
        new_distance = haversine(self.user_location['latitude'], self.user_location['longitude'],
                                  new_hostel.latitude, new_hostel.longitude)
        current_distance = haversine(self.user_location['latitude'], self.user_location['longitude'],
                                     current_node.hostel.latitude, current_node.hostel.longitude)

        # Compare distances and insert accordingly
        if new_distance < current_distance:
            current_node.left = self._insert_recursive(new_hostel, current_node.left)
        else:
            current_node.right = self._insert_recursive(new_hostel, current_node.right)

        return current_node
    
    

    def get_sorted_hostels(self):
        sorted_hostels = []
        self._inorder_traversal(self.root, sorted_hostels)
        print(sorted_hostels)
        for hostel_node in sorted_hostels:
            hostel = hostel_node['hostel']
            distance = hostel_node['distance']
            
            print(f"Hostel Name: {hostel.name}")
            print(f"Hostel Address: {hostel.address}")
   

            
            # Print other details as needed
            print("-" * 20)  # Separator between hostels
          # Add this line to print sorted hostels for verification
        return sorted_hostels

    
  

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            distance = round(haversine(self.user_location['latitude'], self.user_location['longitude'],
                                  node.hostel.latitude, node.hostel.longitude),3)
            if distance<1:
                
                display_distance=str(int(distance*1000))+ ' m'
            else:
                display_distance=str(distance)+' km'
            result.append({'hostel': node.hostel, 'distance':distance,'instance':display_distance})
            self._inorder_traversal(node.right, result)

tree = HostelBinaryTree()
tree.insert_from_database()
sorted_hostels = tree.get_sorted_hostels()