from django.contrib.auth.models import User
from django.db import models


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
    photo = models.ImageField(upload_to='profile_photo/', null=True, blank=True)

    # Academics information
    enrollment = models.CharField(max_length=60)
    admission_year = models.CharField(max_length=10)
    course = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    address = models.TextField()

    librarian_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    # Basic information
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True, default="")
    isbn = models.CharField(max_length=50, blank=True, default="")
    edition = models.CharField(max_length=50, blank=True, default="")
    year_published = models.CharField(max_length=10, blank=True, default="")

    # Classification
    category = models.CharField(max_length=100, blank=True, default="")
    course_code = models.CharField(max_length=50, blank=True, default="")
    shelf_location = models.CharField(max_length=100, blank=True, default="")

    # Stock
    quantity = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    language = models.CharField(max_length=50, blank=True, default="")

    # Extra
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title




