from __future__ import annotations

import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Book, Student



EMAIL_PATTERN = r"^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def home(request):
    return render(request, "index.html")

def help(request):
    return render(request,"help.html")

def register(request):
    return render(request, "accounts/register.html")


def login_page(request):
    if request.method != "POST":
        return render(request, "accounts/login.html")

    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""
    role_input = (request.POST.get("role") or "").strip()  # set by role tabs in template

    if not email or not re.match(EMAIL_PATTERN, email):
        messages.error(request, "Enter a valid email address")
        return redirect("register")

    # Try auth by username=email first (current behavior)
    user = authenticate(request, username=email, password=password)

    # Fallback: some accounts may have email stored as the auth email field
    if user is None:
        user = authenticate(request, email=email, password=password)

    if user is None:
        messages.error(request, "Invalid email or password")
        return render(request, "accounts/login.html")

    login(request, user)

    # role based redirection
    student = Student.objects.filter(user=user).first()

    if not student:
        messages.error(request, "Profile not found")
        return redirect("login")

    if role_input == "librarian" and student.role != "librarian":
        messages.error(request, "You are not authorized as librarian")
        return redirect("login")

    if student.role == "librarian":
        return redirect("lib_dash")

    return redirect("std_dash")


def forget(request):
    return render(request, "accounts/forget.html")


@login_required(login_url="login")
def std_dash(request):
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning ☀️"
    elif hour < 18:
        greeting = "Good Afternoon 🌤️"
    else:
        greeting = "Good Evening 🌙"

    student = Student.objects.filter(user=request.user).first()

    if not student:
        messages.error(request, "Student profile not found")
        return redirect("login")




    context = {
        "greeting": greeting,
        "full_name": request.user.get_full_name(),
        "enrollment": student.enrollment,
        "course": student.course,
        "semester": student.semester,
        "photo": student.photo,
        "student": student,
    }
    return render(request, "dashboard/std_dash.html", context)


def std_register(request):
    if request.method != "POST":
        return render(request, "accounts/register.html")

    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""
    confirm_password = request.POST.get("confirm_password") or ""

    if not email or not re.match(EMAIL_PATTERN, email):
        messages.error(request, "Enter a valid email address")
        return redirect("register")

    if password != confirm_password:
        messages.error(request, "Passwords do not match")
        return render(request, "accounts/register.html")

    if User.objects.filter(username=email).exists():
        messages.error(request, "email already registered")
        return redirect("register")

    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=request.POST.get("first_name") or "",
            last_name=request.POST.get("last_name") or "",
        )

        student = Student.objects.create(
            user=user,
            first_name=request.POST.get("first_name") or "",
            last_name=request.POST.get("last_name") or "",
            dob=request.POST.get("dob"),
            gender=request.POST.get("gender") or "",
            mobile=request.POST.get("mobile") or "",
            enrollment=request.POST.get("enrollment") or "",
            admission_year=request.POST.get("admission_year") or "",
            course=request.POST.get("course") or "",
            semester=request.POST.get("semester") or "",
            address=request.POST.get("address") or "",
            photo=request.FILES.get("photo"),
        )

        messages.success(request, "Registration successful!")
        return redirect("login")
    except Exception as e:
        messages.error(request, f"Registration failed: {str(e)}")
        return render(request, "accounts/register.html")
    
    # librarian login
    
@login_required(login_url="login")
def lib_dash(request):
    student = Student.objects.filter(user=request.user).first()

    if not student or student.role != "librarian":
        messages.error(request, "Access denied")
        return redirect("login")
    
    students = Student.objects.all()
    
    return render(request, 'dashboard/lib_dash.html',{
        'students':students})



def std_login(request):
    # Kept for backward compatibility, but the app uses `login_page`.
    return login_page(request)

#logout logic
def user_logout(request):
    logout(request)
    return redirect("login")

#Adding a book from librarian end

def librarian_dashboard(request):

    # ADD BOOK
    if request.method == "POST":

        # BASIC INFORMATION
        title = request.POST.get("title")
        author = request.POST.get("author")
        publisher = request.POST.get("publisher")
        isbn = request.POST.get("isbn")
        edition = request.POST.get("edition")
        year_published = request.POST.get("year_published")

        # CLASSIFICATION
        category = request.POST.get("category")
        course_code = request.POST.get("course_code")
        shelf_location = request.POST.get("shelf_location")

        # STOCK
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        language = request.POST.get("language")

        # EXTRA
        description = request.POST.get("description")

        # SAVE BOOK
        Book.objects.create(

            # BASIC INFORMATION
            title=title,
            author=author,
            publisher=publisher,
            isbn=isbn,
            edition=edition,
            year_published=year_published,

            # CLASSIFICATION
            category=category,
            course_code=course_code,
            shelf_location=shelf_location,

            # STOCK
            quantity=quantity,
            available=quantity,
            price=price,
            language=language,

            # EXTRA
            description=description
        )

        return redirect('lib_dash')

    # SHOW ALL BOOKS
    books = Book.objects.all()

    context = {
        "books": books
    }

    return render(request, "lib_dash.html", context)

