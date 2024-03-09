from math import radians, sin, cos, sqrt, atan2

def calculate_distance(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0
    print(coord1,coord2)
    # Convert coordinates from degrees to radians
    lat1 = radians(coord1[0])
    # print(lat1)
    lon1 = radians(coord1[1])
    # print(lon1)
    lat2 = radians(coord2[0])
    # print(lat2)
    lon2 = radians(coord2[1])
    # print(lon2)

    # Calculate differences between latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


def read_locations(file_path):
    locations = {}

    with open(file_path, 'r') as file:
        for line in file:
            name, latitude, longitude = line.strip().split(',')
            locations[name] = {'latitude': float(latitude), 'longitude': float(longitude)}

    return locations


def get_coordinates(location, file_path):
    locations = read_locations(file_path)
    
    if location in locations:
        return locations[location]['latitude'], locations[location]['longitude']
    else:
        return 11,11
    
    
def get_recommended_people(latitude, longitude, people, location_file_path):
    recommended_people = []
    threshold=1.0
    for person in people:
        print(person)
        # person_latitude, person_longitude = person['latitude'], person['longitude']
        person_latitude = float(person['latitude'])
        person_longitude = float(person['longitude'])
        # if person_latitude==latitude and person_longitude==longitude:
        if 1==1:

            # print(person_latitude,person_longitude)
            distance = calculate_distance((latitude, longitude), (person_latitude, person_longitude))
            distance=distance/1000.0
            # print(distance)
            if distance<=threshold:
            # if latitude==person_latitude:
            

                recommended_people.append({
                    'name': person['name'].replace('Name: ', ''),
                    'location': person['location'],
                    'image_path': person['image_path'],
                    'distance': distance,
                    'temporary_address': person['temporary_address'],
                    'age': person['age'],
                    'name_of_institute': person['name_of_institute'],
                    'permanent_address': person['permanent_address'],
                    'temporary_address': person['temporary_address'],
                    'bio': person['bio'],
                    'hobbies':person['hobbies']

                    })
        # recommended_people.append(person)
        
    recommended_people.sort(key=lambda x: x['distance'])
    print("hi")
    # print(recommended_people)
    return recommended_people



# def __init__(self, filepath):
#     self.users = {}
#     self.read_users_from_file(filepath)

# def read_users_from_file(self, filepath):
#     with open(filepath, 'r') as file:
#         for user_id, line in enumerate(file, 1):
#                 # Assuming preferences are separated by commas or spaces
#             preferences = list(map(int, line.strip().replace(',', ' ').split()))
#             self.users[str(user_id)] = people(preferences)

# def find_roommates(self):
#     matches = []
#     pq = []
#     user_ids = list(self.users.keys())
#     for i in range(len(user_ids)):
#         for j in range(i + 1, len(user_ids)):
#             user1 = self.users[user_ids[i]]
#             user2 = self.users[user_ids[j]]
#             compatibility_score = user1.calculate_compatibility(user2)
#             heapq.heappush(pq, (-compatibility_score, user1, user2))

#     matched = set()
#     while pq and len(matched) < len(self.users):
#         _, user1, user2 = heapq.heappop(pq)
#         if user1 not in matched and user2 not in matched:
#             user1.match = user2
#             user2.match = user1
#             matches.append((user1, user2))
#             matched.update([user1, user2])

#     return matches
# class User:
#     def __init__(self, preferences):
#         self.preferences = preferences
#         self.match = None

#     def calculate_compatibility(self, other):
#         return sum(abs(a - b) for a, b in zip(self.preferences, other.preferences))
# import heapq

# class RoommateMatcher:
#     def __init__(self, filepath):
#         self.users = {}
#         self.read_users_from_file(filepath)

#     def read_users_from_file(self, filepath):
#         with open(filepath, 'r') as file:
#             for user_id, line in enumerate(file, 1):
#                 # Assuming preferences are separated by commas or spaces
#                 preferences = list(map(int, line.strip().replace(',', ' ').split()))
#                 self.users[str(user_id)] = User(preferences)

#     def find_roommates(self):
#         matches = []
#         pq = []
#         user_ids = list(self.users.keys())
#         for i in range(len(user_ids)):
#             for j in range(i + 1, len(user_ids)):
#                 user1 = self.users[user_ids[i]]
#                 user2 = self.users[user_ids[j]]
#                 compatibility_score = user1.calculate_compatibility(user2)
#                 heapq.heappush(pq, (-compatibility_score, user1, user2))

#         matched = set()
#         while pq and len(matched) < len(self.users):
#             _, user1, user2 = heapq.heappop(pq)
#             if user1 not in matched and user2 not in matched:
#                 user1.match = user2
#                 user2.match = user1
#                 matches.append((user1, user2))
#                 matched.update([user1, user2])

#         return matches
