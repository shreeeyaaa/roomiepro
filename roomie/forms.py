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

