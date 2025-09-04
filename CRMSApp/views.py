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
    all_users = models.AuthModel.objects.all()
    context = {
        "current_user": current_user,
        "all_users": all_users
    }
    return render(request, "dash/dash.html", context)

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
