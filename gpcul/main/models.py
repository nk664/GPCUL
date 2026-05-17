from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Student(models.Model):
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('librarian', 'Librarian'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    


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
    


    librarian_id = models.CharField(max_length= 20, blank = True, null = True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    #login setup 
    
