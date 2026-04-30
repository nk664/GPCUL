from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime


# Create your views here.

def home(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'accounts/register.html')

def login_page(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username = email, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('std_dash')
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'accounts/login.html')
            
    return render(request, 'accounts/login.html')

def forget(request):
    return render(request, 'accounts/forget.html')

@login_required(login_url= 'login')
def std_dash(request):
    hour = datetime.now().hour
    # Initialize greeting based on time of day
    greeting = 'Hello'  # default
    if hour < 12:
        greeting = 'Good Morning ☀️'
    elif hour < 18:
        greeting = 'Good Afternoon 🌤️'
    else: 
        greeting = 'Good Evening 🌙'

    # Get student data from Student model
    try:
        student = Student.objects.get(user=request.user)
        enrollment = student.enrollment
        course = student.course
        semester = student.semester
    except Student.DoesNotExist:
        enrollment = ''
        course = ''
        semester = ''

    context = {
        'greeting': greeting,
        'enrollment': enrollment,
        'course': course,
        'semester': semester,
    }

    return render(request, 'dashboard/std_dash.html', context)

def std_register(request):
    
    if request.method == "POST":
        print("POST data keys:", list(request.POST.keys()))
        print("FILES:", dict(request.FILES))
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        

        if User.objects.filter(username = email).exists():
            
            messages.error(request, "email already registered")
            return redirect('register')
        
        try:
            user = User.objects.create_user(
                username = email,
                email = email,
                password = password,
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),            )
            
            
        

            student_data = {
                'user': user,
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'dob': request.POST.get('dob'),
                'gender': request.POST.get('gender'),
                'mobile': request.POST.get('mobile'),
                'enrollment': request.POST.get('enrollment'),
                'admission_year': request.POST.get('admission_year'),
                'course': request.POST.get('course'),
                'semester': request.POST.get('semester'),
                'address': request.POST.get('address'),
                'photo': request.FILES.get('photo'),
            }

            
            student = Student.objects.create(**student_data)
            
            
            messages.success(request, "Registration successful!")
            
            return redirect('login')
        except Exception as e:
            
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'accounts/register.html')
    
    return render(request, 'accounts/register.html')

def std_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
#check user

        user = authenticate(request, username = email, password = password)
        

        if user is not None:
            login(request, user)
            return redirect('std_dash')
        else:
            messages.error(request, 'invalid email or password')
            
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
