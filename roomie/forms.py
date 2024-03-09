from django import forms

HOBBY_CHOICES = (
    ('singing', 'Singing'),
    ('dancing', 'Dancing'),
    ('painting', 'Painting'),
    ('hiking', 'Hiking'),
    ('gaming', 'Gaming'),
    ('cooking', 'Cooking'),
    ('sports', 'Sports'),
    # Add more choices as needed
)

class UserForm(forms.Form):
    # profile_picture=forms.ImageField()
    name_of_institute=forms.CharField(max_length=100)
    permanent_address=forms.CharField(max_length=100)
    temporary_address=forms.CharField(max_length=100)
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(max_value=100)
    photo = forms.ImageField()
    # location = forms.CharField(max_length=100)
    bio= forms.CharField(max_length=200)
    # hobbies = forms.ChoiceField(choices=HOBBY_CHOICES, widget=forms.CheckboxInput)
    # hobbies = forms.MultipleChoiceField(choices=HOBBY_CHOICES, widget=forms.CheckboxSelectMultiple)
    hobbies = forms.MultipleChoiceField(choices=HOBBY_CHOICES, widget=forms.CheckboxSelectMultiple)


    # passion = forms.CharField(max_length=100)
