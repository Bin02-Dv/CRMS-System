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
    path("repayment/", views.record_repayment, name="repayment"),
    path("approve-loan/<int:id>", views.approve_load, name="approve-loan"),
    
    path("api/send-message/", views.send_message, name="send_message"),
]
