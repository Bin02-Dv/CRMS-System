from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

class AuthModel(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, blank=True)
    
    username = models.CharField(max_length=200, blank=True, unique=True)
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.full_name

class Customer(models.Model):
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, blank=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    home_address = models.TextField(max_length=200, blank=True)
    account_type = models.CharField(max_length=40, blank=True)


class Loan(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=40, blank=True)
    loan_amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    loan_period = models.IntegerField(null=True, default=0)
    interest_rate = models.IntegerField(null=True, default=0)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=40, default='pending')
    due_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.loan_period and not self.due_date:
            self.due_date = date.today() + relativedelta(months=int(self.loan_period))
        super().save(*args, **kwargs)
    
    
    