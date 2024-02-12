# custom_auth.py

from django.contrib.auth.models import User

def custom_authenticate(username, password):
    user = User.objects.filter(username=username).first()

    if user is None:
        return "username_not_found"  # Username does not exist in the database
    elif not user.check_password(password):
        return "incorrect_password"  # Password is incorrect
    else:
        return user  # Authentication successful
