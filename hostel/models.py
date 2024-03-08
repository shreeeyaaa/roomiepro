
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

 
class Diff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, )
    is_student = models.BooleanField(default = True)

    def __str__(self):
        return str(self.user)

class Room(models.Model):
    room_no = models.IntegerField(primary_key=True, unique=True)
    block_no = models.CharField(max_length=1, null=True)
    capacity = models.IntegerField(default=3)
    vacancy = models.IntegerField(default=3)

    def __str__(self):
        return str(self.room_no)

class Student(models.Model):
    # id = models.AutoField(primary_key=True, default=generate_unique_id)

    # join_year     = models.IntegerField(default=2016)
    # join_year     = models.IntegerField(default=2016)
    name   =  models.CharField(max_length = 200, null=True)
    # father_name   =  models.CharField(max_length = 200, null=True)
    # room          = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    GENDER_CHOICES=[
        ('male', 'Male'),
        ('female', 'Female')
    ]
    HOBBIES_CHOICES=[
        ('Singing', 'singing'),
        ('Dancing' , 'dancing'),
        ('Painting' , 'painting'),
        ('Hiking' , 'hiking'),
        ('Gaming' , 'gaming'),
        ('Cooking' , 'cooking'),
        ('Sports' , 'sports'),
    ]
    age           = models.IntegerField(default=20)
    gender        = models.CharField(choices=GENDER_CHOICES, default='male',max_length = 6)
    hobbies       = models.CharField(choices=HOBBIES_CHOICES, default='Singing',max_length= 10)
    name_of_institute=models.CharField(max_length =100,null=True)
    # father_name   =  models.CharField(max_length = 200, null=True)
    # date_of_birth =  models.DateField(null =True, blank = True)
    profile_picture   =  models.FileField(upload_to='profile_picture/', null=True)
    permanent_address       =  models.CharField(max_length = 100,null =True)
    temporary_address       =  models.CharField(max_length = 100,null =True)
    bio          =  models.CharField(max_length = 200,null =True)
    # state         =  models.CharField(max_length = 100,null =True)
    # pincode       = models.IntegerField(default=382009)
    # roll_no       = models.CharField(max_length = 10, primary_key =True,unique = True )
    def __str__(self):
        return str(self.name)

class Change(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason  = models.CharField(max_length = 300)

class Swap(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student1')
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student2')
    reason   = models.CharField(max_length = 300)
    accept   = models.BooleanField(default = False)

