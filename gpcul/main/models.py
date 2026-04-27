from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Student(models.model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    


    # personal information
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='profile_photo/',null = True, blank=True)
    


    #Academics information
    

    enrollment = models.CharField(max_length=60)
    admission_year = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    address = models.TextField()
    


    #login setup 
    

    first_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)