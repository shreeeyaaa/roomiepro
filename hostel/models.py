
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
    join_year     = models.IntegerField(default=2016)
    room          = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    GENDER_CHOICES=[
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender        = models.CharField(choices=GENDER_CHOICES, default='male',max_length = 6)
    father_name   =  models.CharField(max_length = 200, null=True)
    date_of_birth =  models.DateField(null =True, blank = True)
    fee_receipt   =  models.FileField(upload_to='receipt/', null=True)
    address       =  models.CharField(max_length = 100,null =True)
    city          =  models.CharField(max_length = 100,null =True)
    state         =  models.CharField(max_length = 100,null =True)
    pincode       = models.IntegerField(default=382009)
    roll_no       = models.CharField(max_length = 10, primary_key =True,unique = True )
    def __str__(self):
        return str(self.roll_no)

class Change(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason  = models.CharField(max_length = 300)

class Swap(models.Model):
    student1 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student1')
    student2 = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student2')
    reason   = models.CharField(max_length = 300)
    accept   = models.BooleanField(default = False)

class Hostel(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    pricing = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    contact = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    message = models.TextField(null=True,blank = True)
    available = models.BooleanField(null = True,blank = True)
    seater2 = models.IntegerField(blank = True)
    seater3 = models.IntegerField(blank = True)

 

    def __str__(self):
        return self.name

    

    
class HostelImage(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostel_images/')
    
    def __str__(self):
        return f"Image for {self.hostel.name}"


