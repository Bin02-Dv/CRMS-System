from django.shortcuts import render

# Create your views here.

def dash(request):
    return render(request, "dash/dash.html")

def login(request):
    return render(request, "dash/login.html")
