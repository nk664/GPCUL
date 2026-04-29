from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Student
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'accounts/register.html')

def login(request):
    return render(request, 'accounts/login.html')

def forget(request):
    return render(request, 'accounts/forget.html')



def std_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        if User.objects.filter(username = email).exists():
            messages.error(request, "email already registered")
            return redirect('register')
        

        user = User.objects.create_user(
            username = email,
            email = email,
            password = password
            )
        

        Student.objects.create(
            user = user,
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            dob = request.POST.get('dob'),
            gender = request.POST.get('gender'),
            mobile = request.POST.get('mobile'),
            enrollment = request.POST.get('enrollment'),
            admission_year = request.POST.get('admission_year'),
            course = request.POST.get('course'),
            semester = request.POST.get('semester'),
            address = request.POST.get('address'),
            photo = request.FILES.get('photo'),
            
        )
        messages.success(request, "registration successful !")
        
        
        return redirect('login')
    return render (request, 'accounts/register.html')