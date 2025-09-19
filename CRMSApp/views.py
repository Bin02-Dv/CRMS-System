from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.utils.timezone import now
import json, re

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect("/login/")

@login_required(login_url='/login/')
def dash(request):
    current_user = request.user
    customers = models.Customer.objects.all().count()
    loans = models.Loan.objects.all()
    amount = [loan.loan_amount for loan in loans]
    total_amount = sum(amount)
    context = {
        "current_user": current_user,
        "total_customers": f"{customers:,}",
        "total_loans": f"{loans}",
        "total_amount": f"{total_amount:,}"
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
    loans = models.Loan.objects.all()
    context = {
        "current_user": current_user,
        "loans": loans
    }
    return render(request, "dash/customer-communication.html", context)

@login_required(login_url='/login/')
def loan_management(request):
    current_user = request.user
    customers = models.Customer.objects.all()
    loans = models.Loan.objects.all()
    coms = models.Communication.objects.all().order_by("-date_sent")[:2]
    
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
        "loans": loans,
        "coms": coms
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


@login_required(login_url='/login/')
@csrf_exempt
def record_repayment(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        payment_amount = request.POST.get("payment_amount")

        if not customer_id or not payment_amount:
            return JsonResponse({"success": False, "message": "All fields are required!"})

        try:
            loan = models.Loan.objects.get(customer_id=customer_id, status="approved")
        except models.Loan.DoesNotExist:
            return JsonResponse({"success": False, "message": "No approved loan found for this customer."})

        payment_amount = Decimal(payment_amount)

        models.Repayment.objects.create(
            loan=loan,
            amount=payment_amount,
            received_by=request.user
        )

        loan.loan_amount -= payment_amount
        if loan.loan_amount <= 0:
            loan.status = "completed"
            loan.loan_amount = 0
        loan.save()

        return JsonResponse({
            "success": True,
            "message": f"Payment of ₦{payment_amount} recorded successfully!",
            "balance": float(loan.loan_amount),
            "next_due": str(loan.due_date)
        })

    return JsonResponse({"success": False, "message": "Invalid request method."})

def approve_load(request, id):
    try:
        get_loan = models.Loan.objects.get(id=id)
    except models.Loan.DoesNotExist:
        return None, "ID not found!"
    
    get_loan.status = 'approved'
    get_loan.save()
    return redirect('/loan-management/')

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)

        channel = data.get("channel")
        message = data.get("message")
        customer = data.get("customer")
        amount = data.get("amount")
        date = data.get("date")

        models.Communication.objects.create(
            customer_name=customer,
            message=message,
            channel=channel
        )

        return JsonResponse({
            "status": "success",
            "channel": channel,
            "message": message,
            "customer": customer,
            "amount": amount,
            "date": date
        })