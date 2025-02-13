from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    choices = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=100, choices=choices, default='employee')
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, limit_choices_to={'role':'manager'}, related_name='subordinates')

    def clean(self):
        if self.role == 'manager' and self.supervisor == self:
            raise ValidationError({'supervisor':'You cannot assign yourself as a supervisor'})
    
    @property
    def is_employee(self):
        if self.role == 'employee':
            return True
        return False
    @property
    def is_manager(self):
        if self.role == 'manager':
            return True
        return False
    @property
    def is_admin(self):
        if self.role == 'admin':
            return True
        return False
    
    def __str__(self):
        return self.username


class ExpenseCategory(models.Model):
    expense_category = models.CharField(max_length=60, unique=True)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    
    def clean(self):
        if self.limit<=0:
            raise ValidationError({'limit':'Limit must be greater than Zero'})
        
    def __str__(self):
        return self.expense_category
    
    
class ExpenseClaim(models.Model):
    status_choices = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empallclaims')
    expense_type = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='allclaims')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    claim_description = models.TextField()
    receipt = models.FileField(upload_to='receipts')
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    manager_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.amount:
            try:
                self.expense_type
            except Exception as e:
                raise ValidationError({'expense_type':'Please select an expense_type'})
            if self.amount>self.expense_type.limit:
                raise ValidationError({'amount':'Amount cannnot be greater than the max limit'})
            
    def __str__(self):
        return f'{self.employee.username.title()} requested claim of amount: ({self.amount}) for {self.expense_type} at {self.created_at.date()}'
    
    