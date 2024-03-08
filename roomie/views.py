from django.shortcuts import render, redirect
from .forms import UserForm
import os
from .utils import get_coordinates, read_locations, calculate_distance, get_recommended_people
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'user_data.txt')
location_file_path = os.path.join(BASE_DIR, 'location_data.txt')

# Create your views here.
def add_roomie(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            print("hello")
            # Process the form data and save it to a file
            name = form.cleaned_data['name']
            photo = form.cleaned_data['photo']
            filename = f"{name.lower().replace(' ', '_')}.jpg"
            upload_path = os.path.join('media', 'user_photos', filename)
            with open(upload_path, 'wb') as file:
                for chunk in photo.chunks():
                    file.write(chunk)
                    
                    
            location = form.cleaned_data['location']
            coordinates = get_coordinates(location, location_file_path)
            # passion = form.cleaned_data['passion']
            with open('user_data.txt', 'a') as file:  # 'a' mode to append data to the file
                file.write(f"Name: {name}, Location: {location}, Latitude: {coordinates[0]}, Longitude: {coordinates[1]}\n")
                # file.write(f"Name: {name}, Location: {location}, Pasion: {passion}\n")
            return redirect('/roomie/show_roomies')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})


def show_roomies(request):
    people = []

    with open(file_path, 'r') as file:
        for line in file:
            components = line.strip().split(', ')
            name = components[0].split(': ')[1]
            location = components[1].split(': ')[1]
            latitude = float(components[2].split(': ')[1])
            longitude = float(components[3].split(': ')[1])
            
            username = name.replace('Name: ', '').lower().replace(' ', '_')
            image_path = f"media/user_photos/{username}.jpg"
            people.append({'name': name.replace('Name: ', ''), 'location': location, "latitude": latitude, "longitude": longitude, 'image_path': image_path})

    if request.method == 'POST' and 'location' in request.POST:
        selected_location = request.POST['location']
        request_latitude, request_longitude = get_coordinates(selected_location, location_file_path)
        # recommended_people = [person for person in people if person["location"].lower().strip() == selected_location.lower().strip()]
        recommended_people = get_recommended_people(request_latitude, request_longitude, people, location_file_path)
    else:
        recommended_people = people
    locations = [
        "Kathmandu",
        "Baneshwor",
        "Lalitpur",
        "Jhamsikhel",
        "Sinamangal"
    ]
    return render(request, 'roomies.html', {'people': recommended_people,"locations": locations})
