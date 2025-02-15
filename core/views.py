from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    """Render the home page."""
    return render(request, "core/home.html")

def passenger_register(request):
    """Handle passenger registration."""
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("passenger_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("passenger_register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect("passenger_login")

    return render(request, "core/passenger_register.html")

def passenger_login(request):
    """Handle passenger login."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("passenger_login")

    return render(request, "core/passenger_login.html")

def passenger_logout(request):
    """Log out the passenger."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")
