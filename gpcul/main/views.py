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
    print("=== std_register CALLED ===")
    print(f"Method: {request.method}")
    if request.method == "POST":
        print("POST data keys:", list(request.POST.keys()))
        print("FILES:", dict(request.FILES))
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password len: {len(password or '')}")
        

        if User.objects.filter(username = email).exists():
            print("Email exists, error message sent")
            messages.error(request, "email already registered")
            return redirect('register')
        
        try:
            user = User.objects.create_user(
                username = email,
                email = email,
                password = password
            )
            print(f"User created: {user.username}")

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
            print("Student data:", {k: v[:20] + '...' if isinstance(v, str) and len(v)>20 else v for k,v in student_data.items()})
            
            student = Student.objects.create(**student_data)
            print(f"Student created ID: {student.id}")
            
            messages.success(request, "Registration successful!")
            print("SUCCESS - redirecting to login")
            return redirect('login')
        except Exception as e:
            print(f"ERROR creating user/student: {e}")
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'accounts/register.html')
    print("GET request - rendering form")
    return render(request, 'accounts/register.html')
