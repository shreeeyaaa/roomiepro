from django import forms

class UserForm(forms.Form):
    name = forms.CharField(max_length=100)
    photo = forms.ImageField()
    location = forms.CharField(max_length=100)
    # passion = forms.CharField(max_length=100)
