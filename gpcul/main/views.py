from __future__ import annotations

import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Student


EMAIL_PATTERN = r"^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def home(request):
    return render(request, "index.html")


def register(request):
    return render(request, "accounts/register.html")


def login_page(request):
    if request.method != "POST":
        return render(request, "accounts/login.html")

    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""

    if not email or not re.match(EMAIL_PATTERN, email):
        messages.error(request, "Enter a valid email address")
        return redirect("register")

    user = authenticate(request, username=email, password=password)
    if user is None:
        messages.error(request, "Invalid email or password")
        return render(request, "accounts/login.html")

    login(request, user)


    #role based redirection
    try:
        student = student.object.get(user=user)


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

    try:
        student = Student.objects.get(user=request.user)
        full_name = f"{student.first_name}{student.last_name}"
        enrollment = student.enrollment
        course = student.course
        semester = student.semester
    except Student.DoesNotExist:
        enrollment = ""
        course = ""
        semester = ""

    context = {
        "greeting": greeting,
        "full_name": request.user.get_full_name(),
        "enrollment": enrollment,
        "course": course,
        "semester": semester,
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
#def lib_dash(request):
  #  return render(request, 'dashboard/lib_dash.html' )


def std_login(request):
    # Kept for backward compatibility, but the app uses `login_page`.
    return login_page(request)


def user_logout(request):
    logout(request)
    return redirect("login")

