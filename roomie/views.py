from django.shortcuts import render, redirect
from .forms import UserForm
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'user_data.txt')

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
            # passion = form.cleaned_data['passion']
            with open('user_data.txt', 'a') as file:  # 'a' mode to append data to the file
                file.write(f"Name: {name}, Location: {location}\n")
                # file.write(f"Name: {name}, Location: {location}, Pasion: {passion}\n")
            return redirect('/roomie/show_roomies')
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})


def show_roomies(request):
    people = []
    with open(file_path, 'r') as file:
        for line in file:
            name, location = line.strip().split(', Location: ')# add fields like passion here to read from file
            username = name.replace('Name: ', '').lower().replace(' ', '_')
            image_path = f"media/user_photos/{username}.jpg"
            people.append({'name': name.replace('Name: ', ''), 'location': location, 'image_path': image_path})
            
    recommended_people = []
    for person in people:
        if person["location"].lower().strip() == 'ktm':
            recommended_people.append(person)
            
    return render(request, 'roomies.html', {'people': recommended_people})