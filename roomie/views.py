from django.shortcuts import render, redirect
from .forms import UserForm
import os
from .utils import get_coordinates, read_locations, calculate_distance, get_recommended_people

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'user_data.txt')
# file_path = os.path.join(BASE_DIR, 'user_data.txt')
location_file_path = os.path.join(BASE_DIR, 'location_data.txt')

# Create your views here.
def add_roomie(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            print("hello")
            # Process the form data and save it to a file
            # location= form.cleaned_data['location']
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            name_of_institute = form.cleaned_data['name_of_institute']
            permanent_address = form.cleaned_data['permanent_address']
            temporary_address = form.cleaned_data['temporary_address']
            bio = form.cleaned_data['bio']
            photo = form.cleaned_data['photo']
            hobbies= form.cleaned_data['hobbies']
            filename = f"{name.lower().replace(' ', '_')}.jpg"
            upload_path = os.path.join('media', 'user_photos', filename)
            with open(upload_path, 'wb') as file:
                for chunk in photo.chunks():
                    file.write(chunk)
                    
            coordinates = get_coordinates(temporary_address, location_file_path)       
            # location = form.cleaned_data['location']
            # passion = form.cleaned_data['passion']
            with open('user_data.txt', 'a') as file:  # 'a' mode to append data to the file
                file.write(f"Name: {name}, Age: {age}, Name_of_institute: {name_of_institute}, permanent_address: {permanent_address}, temporary_address: {temporary_address}, bio: {bio}, hobbies: {hobbies}, Latitude: {coordinates[0]}, Longitude: {coordinates[1]} \n")
                # file.write(f"Name: {name}, Location: {location}, Pasion: {passion}\n")
            return redirect('/roomie/show_roomies')
        else:
            print(form.errors)
            # return render(request, 'indexx.html')
    else:
       
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})



def show_roomies(request):
    people = []

    file_path = "user_data.txt"  # Define the file path here

    with open(file_path, "r") as file:
        for line in file:
            fields = line.strip().split(', ')
            # print(fields)
            name = age = name_of_institute = permanent_address = temporary_address = bio = hobbies = location = latitude = longitude= None
            for field in fields:
                # split_result = field.split(': ')
                # print("Field before splitting:", field)
                split_result = field.split(': ')
                print("Split result:", split_result)
                if len(split_result) == 2:
                    key, value = split_result
                    if key == 'Name':
                        name = value
                    elif key == 'Age':
                        age = value
                    elif key == 'Location':
                        location = value
                    elif key == 'Name_of_institute':
                        name_of_institute = value
                    elif key == 'permanent_address':
                        permanent_address = value
                    elif key == 'temporary_address':
                        temporary_address = value
                    elif key == 'bio':
                        bio = value
                    elif key == 'hobbies':
                    # Extract hobbies as a list
                        hobbies = value.strip('[]').split(', ')
                    elif key =='Location':
                        location= value
                    elif key =='Latitude':
                        latitude= value
                    elif key == 'Longitude':
                        longitude= value

            username = name.lower().replace(' ', '_')
            image_path = f"media/user_photos/{username}.jpg"

            people.append({
                'name': name,
                'age': age,
                'name_of_institute': name_of_institute,
                'permanent_address': permanent_address,
                'temporary_address': temporary_address,
                'bio': bio,
                'hobbies': hobbies,
                'location': location,
                'image_path': image_path,
                'latitude': latitude,
                'longitude':longitude

            })

    # print(people)
    # No need to read the file again
    recommended_people = []

    if request.method == 'POST' and 'location' in request.POST:
        selected_location = request.POST['location']
        print(selected_location)
        request_latitude, request_longitude = get_coordinates(selected_location, location_file_path)
        print(request_latitude, request_longitude)
        # recommended_people = [person for person in people if person["location"].lower().strip() == selected_location.lower().strip()]
        recommended_people = get_recommended_people(request_latitude, request_longitude, people, location_file_path)
        print(recommended_people)
    else:
        recommended_people = people
    locations = [
        "Kathmandu",
        "Baneshwor",
        "Lalitpur",
        "Jhamsikhel",
        "Sinamangal"
    ]
    return render(request, 'roomies.html', {'people': recommended_people,"locations": locations, temporary_address:"temporary_address"})
    # print (people)
    # for person in people:
    #     if person["name_of_institute"].lower().strip() == 'pulchowk campus':
    #         recommended_people.append(person)

    # return render(request, 'roomies.html', {'people': recommended_people})


def show_profiles(request):
    # Assume users_data is a list of dictionaries, each containing data for a user
    people = []

    file_path = "user_data.txt"  # Define the file path here
    

    with open(file_path, "r") as file:
        for line in file:
            fields = line.strip().split(', ')
            # print(fields)
            name = age = name_of_institute = permanent_address = temporary_address = bio = hobbies = location = None
            for field in fields:
                # split_result = field.split(': ')
                # print("Field before splitting:", field)
                split_result = field.split(': ')
                # print("Split result:", split_result)
                if len(split_result) == 2:
                    key, value = split_result
                    if key == 'Name':
                        name = value
                    elif key == 'Age':
                        age = value
                    elif key == 'Location':
                        location = value
                    elif key == 'Name_of_institute':
                        name_of_institute = value
                    elif key == 'permanent_address':
                        permanent_address = value
                    elif key == 'temporary_address':
                        temporary_address = value
                    elif key == 'bio':
                        bio = value
                    elif key == 'hobbies':
                    # Extract hobbies as a list
                        hobbies = value.strip('[]').split(', ')
                    elif key =='Location':
                        location= value

            username = name.lower().replace(' ', '_')
            image_path = f"media/user_photos/{username}.jpg"

            people.append({
                'name': name,
                'age': age,
                'name_of_institute': name_of_institute,
                'permanent_address': permanent_address,
                'temporary_address': temporary_address,
                'bio': bio,
                'hobbies': hobbies,
                'location': location,
                'image_path': image_path
            })
    # users_data = [
    #     {"name": "User 1", "age": 25, "location": "Location 1", "image_path": "/path/to/image1.jpg"},
    #     {"name": "User 2", "age": 30, "location": "Location 2", "image_path": "/path/to/image2.jpg"},
    #     # Add more user data as needed
    # ]

    return render(request, 'users.html', {'users_data': people})