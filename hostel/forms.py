
import re
from django import forms
from django.contrib.auth.models import User
from .models import Student, Diff, Room
from django.core.validators import EmailValidator
from django.utils.timezone import datetime


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email is already taken!!')
        if not EmailValidator(email):
            raise forms.ValidationError('Email does not exist!')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(
                'Password length at least 8 characters')
        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'[A-Za-z]{3,}', first_name):
            raise forms.ValidationError('Name is not valid!')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'[A-Za-z]{3,}', last_name):
            raise forms.ValidationError('Name is not valid!')
        return last_name


class DiffForm(forms.ModelForm):
    class Meta:
        model = Diff
        fields = ('is_student',)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'age', 'hobbies', 'name_of_institute',
                  'permanent_address', 'temporary_address', 'bio', 'profile_picture')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not (age > 15 and age <= 70):
            raise forms.ValidationError('Please enter valid age')
        return age

    # def clean_pincode(self):
    #     pincode = self.cleaned_data.get('pincode')
    #     if not len(str(pincode)) == 6:
    #         raise forms.ValidationError('Please enter valid Pincode')
    #     return pincode

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'[A-Za-z]{3,}', name):
            raise forms.ValidationError('Name is not valid!')
        return name



class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('room_no',)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignInForm(forms.Form):
    username = forms.CharField(max_length=50)
    email= forms.EmailField()
    password= forms.CharField(widget=forms.PasswordInput)