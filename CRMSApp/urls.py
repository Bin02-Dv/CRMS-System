from django.urls import path
from . import views

urlpatterns = [
    path("dash/", views.dash, name="dash"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("user-management/", views.user_management, name="user-management"),
    path("loan-management/", views.loan_management, name="loan-management"),
    path("customer-registration/", views.customer_registration, name="customer-registration"),
    path("customer-communication/", views.customer_communication, name="customer-communication"),
    path("report/", views.report, name="report"),
]
