from math import radians, sin, cos, sqrt, atan2

def calculate_distance(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1 = radians(coord1[0])
    lon1 = radians(coord1[1])
    lat2 = radians(coord2[0])
    lon2 = radians(coord2[1])

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

    for person in people:
        person_latitude, person_longitude = person['latitude'], person['longitude']
        distance = calculate_distance((latitude, longitude), (person_latitude, person_longitude))
        recommended_people.append({
            'name': person['name'].replace('Name: ', ''),
            'location': person['location'],
            'image_path': person['image_path'],
            'distance': distance
        })

    recommended_people.sort(key=lambda x: x['distance'])
    print(recommended_people)

    return recommended_people