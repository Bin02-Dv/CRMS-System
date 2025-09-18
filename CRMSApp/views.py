from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required(login_url='/login/')
def dash(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "dash/dash.html", context)

@login_required(login_url='/login/')
def customer_registration(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "dash/customer-registration.html", context)

@login_required(login_url='/login/')
def customer_communication(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "dash/customer-communication.html", context)

@login_required(login_url='/login/')
def loan_management(request):
    current_user = request.user
    context = {
        "current_user": current_user
    }
    return render(request, "dash/loan-management.html", context)

@login_required(login_url='/login/')
def user_management(request):
    current_user = request.user
    all_users = models.AuthModel.objects.all()
    
    if request.method == 'POST':
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        role = request.POST.get("role", "")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        
        if models.AuthModel.objects.filter(email=email).exists():
            return JsonResponse({
                "message": f"Sorry this email {email} already exist!!",
                "success": False
            })
        elif confirm_password != password:
            return JsonResponse({
                "message": "password and confirm password missed matched!!",
                "success": False
            })
        else:
            models.AuthModel.objects.create_user(
                full_name=full_name, email=email, phone_number=phone_number, role=role, password=password, username="None"
            )
            return JsonResponse({
                "message": "User Added successfully...",
                "success": True
            })
    context = {
        "current_user": current_user,
        "all_users": all_users
    }
    return render(request, "dash/user-management.html", context)

@login_required(login_url='/login/')
def report(request):
    current_user = request.user
    context = {
        "current_user": current_user,
    }
    return render(request, "dash/report.html", context)

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        
        user = models.AuthModel.objects.filter(email=email).first()
        
        if user is not None:
            if user.check_password(password):
                auth.login(request, user)
                return JsonResponse({
                    "message": "Login successfully...",
                    "success": True
                })
            else:
                return JsonResponse({
                    "message": "Incorrect Password!!",
                    "success": False
                })
        else:
            return JsonResponse({
                "message": "Invalid Email!!",
                "success": False
            })
    return render(request, "dash/login.html")
