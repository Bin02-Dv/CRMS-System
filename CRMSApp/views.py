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
    
    all_customers = models.Customer.objects.all()
    
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        home_address = request.POST.get("address")
        account_type = request.POST.get("account_type")
        
        if not all([full_name, email, phone_number, home_address, account_type]):
            return JsonResponse({
                "message": "All Fields are required!!",
                "success": False
            })
        elif models.AuthModel.objects.filter(email=email).exists():
            return JsonResponse({
                "message": f"Sorry this a customer with this email {email} already exist!!",
                "success": False
            })
        else:
            models.Customer.objects.create(
                full_name=full_name, email=email, phone_number=phone_number, home_address=home_address, account_type=account_type
            )
            return JsonResponse({
                "message": "Customer registration completed successfully...",
                "success": True
            })
    context = {
        "current_user": current_user,
        "all_customers": all_customers
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
    customers = models.Customer.objects.all()
    loans = models.Loan.objects.all()
    
    if request.method == 'POST':
        customer_id = request.POST.get("customer")
        loan_type = request.POST.get("loan_type")
        loan_amount = request.POST.get("loan_amount")
        loan_period = request.POST.get("loan_period")
        interest_rate = request.POST.get("interest_rate")
        
        if not all([customer_id, loan_type, loan_amount, loan_period, interest_rate]):
            return JsonResponse({
                "message": "All Fields are required!!",
                "success": False
            })
        else:
            try:
                customer = models.Customer.objects.get(id=customer_id)
            except models.Customer.DoesNotExist:
                return JsonResponse({
                    "message": f"Sorry we couldn't find any user with the ID - {customer_id}",
                    "success": False
                })
            
            models.Loan.objects.create(
                customer=customer, loan_type=loan_type, loan_amount=loan_amount, loan_period=loan_period, interest_rate=interest_rate
            )
            return JsonResponse({
                "message": f"Loan for the customer {customer.full_name} has been created successfully....",
                "success": True
            })
        
    context = {
        "current_user": current_user,
        "customers": customers,
        "loans": loans
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
